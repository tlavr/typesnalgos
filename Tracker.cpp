/*
 * Tracker.cpp
 *
 *  Created on: 24.06.2011
 *      Author: VTV
 *      Edited on 02.08.2019
 *      by: Lavrukhin Timur
 */

#include <xdc/std.h>
#include <map>
#include <cmath>
#include <iostream>
#include <c6x.h>

#include "Board/Pocket.h"
#include "IntMath/Fft.h"
#include "Board/UartPort.h"

#include "IntMath/Copy.h"
#include "Copy.h"
#include "IntMath/RcFilter.h"
#include "IntMath/Util.h"
#include "Gnss/Antenna.h"
#include "Const.h"
#include "Mail.h"
#include "LocateBoard.h"
#include "Tracker.h"
#include "Gnss/Drone.h"
#include "IntMath/Twiddle.h"
#include "LocalParams.h"
#include "Bios/Clock.h"

TrackVars trackvars[corrN];
DLLFilter DLLFilts[corrN];
FPLLFilter FPLLFilts[corrN];

/*
const UShort EPL_OutNum = 10000;
#pragma DATA_SECTION(".ddr")
#pragma DATA_ALIGN(8)
Complex32 EPL_OutVals[3][EPL_OutNum];
#pragma DATA_SECTION(".ddr")
#pragma DATA_ALIGN(8)
UShort EPLPara[3][EPL_OutNum];
#pragma DATA_SECTION(".ddr")
#pragma DATA_ALIGN(8)
Float EPLSampleShift[EPL_OutNum]; */

namespace {

// added by LT
//Complex32 BSBuf[B4Stmp];
//Complex32 BitSyncCor[NBits4Sync];
// end of adding

const UInt prio = 9; // priority of the tracker among all tasks
const Int tauAmpl = 6; // amplitude of the channels
Int tauIq = 6; // for filtering the phase difference
Int tauConvol = 1; // for convolution setting  - rc filter para
Int threshQual0 = 50; // threshold for quality 0 - thresholds for raw data
Int threshQual1 = 50; // -||-  - for filtered data
Int badMax0 = 5; // number of samples for thr0
Int badMax1 = 1; // -||- for 1
UInt skipSv = 0; // skip SV additional parameter bit mask of the SV for skipping
Int32	elMin = 15; // minimum degrees above the horizont for tracking the SV

const Int tauFreq = 6, tauPhase = 2; //  for PLL
const Int tau_bit = 20; // c/a codes for one bit
const Int tau_upd = 20;  // ?
const Int channel = 3; // physical channel index ?

enum StateDemod { //for state of the tracking process -- why these numbers?
	none = 0,
	tracker_add = 1,
	tuner_upd = 2,
	demod_upd = 4,
	found_one_bit_edge = 12,
	found_all_bit_edge = 60
};

struct CorrRegs {
    volatile UInt32 pos[32]; // NCO for code
    volatile Int32 doppler[32]; // NCO freq
    volatile UInt32 sv[32]; // SV number?
};




Ptr const corrAddr = static_cast<UInt8*>(Chip::Emif::address[Chip::Emif::ce2]) + 0x24000; //address of the correlation memory registers
CorrRegs* const regs = static_cast<CorrRegs*>(corrAddr); // inside transform of address

Gnss::Drone::Params& params = Gnss::Drone::Locate().GetParams(); // get params
Int32 tempCnt = 0; // ?
Int32 tempLock = 100; // ?

inline UInt GetSinCos(Int doppler)
{
	return UInt((268698 * doppler) >> 7); // 2^32 * doppler frequency ./ 2^7 = 2.046 MHz ??
}

struct Demod {
	Complex32 phase, sum;
	Int32 freq;
    Int counter, bitCount, bitSkip, bitZnak;

    Demod(): phase(1), sum(0), freq(0), counter(0), bitCount(0), bitSkip(0), bitZnak(0) {}
};

struct Item { //some SV parameters
	Int corr;
	IntMath::RcFilter<Complex32> iq01, iq02;
	Int quality;
	Int badCount0, badCount1;
	Int skipCount;
	Int count, flag;
	Demod dmd[channel];
	IntMath::RcFilter<UInt32> cn0, amplitude;

    Item(): iq01(tauIq, 0), iq02(tauIq, 0), badCount0(0), badCount1(0),
    			quality(0), skipCount(0), count(0), flag(0), cn0(6, 0), amplitude(3, 0) {}
};

// added by LT

/*typedef std::map<Int, DLLFilter> DLLFilt;
typedef std::map<Int, FPLLFilter> FPLLFilt;
typedef std::map<Int, TrackVars> trackVars;
DLLFilt DLLFilts;
FPLLFilt FPLLFilts;
trackVars trackvars;
//DLLFilter DLLFilts[corrN];
//FPLLFilter FPLLFilts[corrN];*/

// end of adding

typedef std::map<Int, Item> Items;
typedef Items::iterator ItemsIterator;
Items items;

IntMath::RcFilter<UInt32> amplitude0(tauAmpl), amplitude1(tauAmpl), amplitude2(tauAmpl);
IntMath::RcFilter<UInt32>* amplPtr[3] = {&amplitude0, &amplitude1, &amplitude2};

class Convolution: public IntMath::RcFilter<Complex32> {
public:
	Convolution(): IntMath::RcFilter<Complex32>(tauConvol) {}
};


#pragma DATA_ALIGN(8)
Convolution convolution[corrN][corrL];

#pragma DATA_ALIGN(8)
Complex32 updConvol[corrN][corrL];

/*
Ptr const switchAddr = static_cast<UInt8*>(Chip::Emif::address[Chip::Emif::ce2]) + 0x24;
UInt32* const switchReg = static_cast<UInt32*>(switchAddr);
UInt32	switchData = 0;
*/
} // namespace

Float abs_for_cn0[corrN]; //

Complex32 rawIq[3]; // additional variable

//------------------------------------------------------

Tracker::Tracker(Bios::Mailbox& dataBox, Bios::Mailbox& controlBox, Bios::Mailbox& demodBox): // dataBox - from engine, controlBox - from Search,
		ControlledHandler(dataBox, controlBox, prio),
		satellites(Gnss::Satellites::Locate()),
		led(LocateBoard().Led()),
		demodBox(demodBox),
		mode(0), graph(0)
{

//	*switchReg = 0;

}

Tracker::Params Tracker::GetParams()
{
	Params params;
	params.tauIq = tauIq;
	params.tauConvol = tauConvol;
	params.threshQual0 = threshQual0;
	params.threshQual1 = threshQual1;
	params.badMax0 = badMax0;
	params.badMax1 = badMax1;
	params.skipSv = skipSv;
	params.elMin = elMin;
	return params;
}

Void Tracker::SetParams(const Tracker::Params& params)
{
	tauIq = params.tauIq;
	tauConvol = params.tauConvol;
	threshQual0 = params.threshQual0;
	threshQual1 = params.threshQual1;
	badMax0 = params.badMax0;
	badMax1 = params.badMax1;
	skipSv = params.skipSv;
	elMin = params.elMin;
	for (Int i = 0; i < corrN; ++i) {
		for (Int j = 0; j < corrL; ++j) {
			convolution[i][j].Setup(tauConvol);
		}
	}
}

Void Tracker::SetMode(const Int setMode) // set tracking mode of SV to initial (tracker_add)
{
	mode = (setMode & 1);
	if (!mode){
		for(Int sv = Gnss::Gps::svFirst; sv <= Gnss::Gps::svLast; sv++)
		{
			Int ind = Gnss::Satellites::Index(Gnss::gps, sv);
			if(satellites[ind].GetParams().flag >= 1)
				satellites[ind].GetParams().flag = 1;
		}
	}
}

Void Tracker::Prolog()
{
}

Void Tracker::Control(Bios::Mail* mail)
{
//	led.On();
	ControlMail* controlMail = static_cast<ControlMail*>(mail);
	index = controlMail->index;

	switch (controlMail->command) {
	case cmdTrack:
		AddSv();
		busy = FALSE;
		break;

	default:
		busy = FALSE;
		break;

	} // switch

//	led.Off();
}

Void Tracker::Process(Bios::Mail* mail)
{

	//	led.On();
	CorrMail* dataMail = static_cast<CorrMail*>(mail);
	address = dataMail->address;
	count = dataMail->count;


	if ((count & 0x3FF) == 0) { // ??
//		led.Toggle();
//		DebugLog();
	}

	params.temperature = tempCnt; // ?? control of the dsp temperature?
	tempCnt ++;
	if(tempCnt == tempLock){
//		led.Toggle();
		tempLock += 100;
	}

	for(Int sv = Gnss::Gps::svFirst; sv <= Gnss::Gps::svLast; sv++)
	{
		Int ind = Gnss::Satellites::Index(Gnss::gps, sv);

		if (items.count(ind) == 0) continue;

		index = ind;
		corr = items[index].corr;

		for(Int32 ii = 0; ii < corrV; ii++) // реорганизаци€ в нужном пор€дке данных с коррел€тора
		{
			Copy(address + corr * corrC + ii, corrData[ii], corrL, corrC * corrN);
		}
/*// can use for debug messages or display some data
		std::stringstream& ss = LocalParams::Locate().GetSS();
		Int32 tt = Bios::Clock::GetTicks();
		ss << "a(" << tt << ") = complex(" << corrData[0][corrL >> 1].re << ", " << corrData[0][corrL >> 1].im << ");" << std::endl;
		LocalParams::Locate().SetLog();
*/
		Gnss::Satellite& satellite = satellites[index];
		Int flag = satellite.GetParams().flag;

		//---- added by LT
		Item& item = items[index];
		TrackVars& tv = trackvars[item.corr];
		if (satellite.GetState() == Gnss::Satellite::found) { // first update
			item.skipCount ++;
			if(item.skipCount == 20){
				satellite.SetState(Gnss::Satellite::tracked);
				item.skipCount = 0;		// кто-то ставит ещЄ статус found
			}
//			continue;
		}
		else
		{
		Gnss::Satellite::Params& params = satellite.GetParams();
		const Gnss::Drone::Params& paramsGPS = Gnss::Drone::Locate().GetParams();
		Double el = params.elevation.Degrees();
		if( el < (double)elMin){
		//		std::cout << "time: " << paramsGPS.tGps <<  " remove 10.0: sv " << sv << " corr " << corr << std::endl;
			RemoveSv();
			return;
		}

		const Int center = (corrL >> 1);
		tv.CurEPLindx = tv.CACounter % 40;
		tv.EPLCorVals[tv.CurEPLindx][0] = /*IntMath::Normalize*/(corrData[0][center-1]); // Early надо ли нормалайз делать?
		tv.EPLCorVals[tv.CurEPLindx][1] = /*IntMath::Normalize*/(corrData[0][center]);  // Prompt
		tv.EPLCorVals[tv.CurEPLindx][2] = /*IntMath::Normalize*/(corrData[0][center+1]);  // Late

		// дампим значени€ с коррел€торов

	/*	if (tv.OutputCount_corr < EPL_OutNum)
		{
			/*EPLPara[0][tv.OutputCount_corr] = index;
			EPLPara[1][tv.OutputCount_corr] = tv.CurrDopplerFreq;
			EPLPara[2][tv.OutputCount_corr] = tv.CACounter;
			EPLSampleShift[tv.OutputCount_corr] = tv.DLL.SampleShift;
			EPL_OutVals[0][tv.OutputCount_corr] = tv.EPLCorVals[tv.CurEPLindx][0];
			EPL_OutVals[1][tv.OutputCount_corr] = tv.EPLCorVals[tv.CurEPLindx][1];
			EPL_OutVals[2][tv.OutputCount_corr] = tv.EPLCorVals[tv.CurEPLindx][2];

			std::stringstream& ss = LocalParams::Locate().GetSS();
			Int32 tt = Bios::Clock::GetTicks();
			ss << "|SV:" << index << "|CACount:" << tv.CACounter << "|CurrFreq:" << tv.CurrDopplerFreq << "|SampleShift:"<< satellite.GetPosition() \
			<< "|EcorrRe:" << tv.EPLCorVals[tv.CurEPLindx][0].re << "|EcorrIm:" << tv.EPLCorVals[tv.CurEPLindx][0].im << "|PcorrRe:" << tv.EPLCorVals[tv.CurEPLindx][1].re << "|PcorrIm:" << tv.EPLCorVals[tv.CurEPLindx][1].im \
			<< "|LcorrRe:" << tv.EPLCorVals[tv.CurEPLindx][2].re << "|LcorrIm:" << tv.EPLCorVals[tv.CurEPLindx][2].im << "|" << std::endl << std::endl; //"|DLL.NCOStep:" << tv.DLL.NCOStep << "|FPLL.NCOStep:" << tv.FPLL.NCOStep << std::endl;
			LocalParams::Locate().SetLog();

			tv.OutputCount_corr++;
		}*/
		/*else
		{
			for (int ii = 0; ii < EPL_OutNum; ii++)
			{
			std::stringstream& ss = LocalParams::Locate().GetSS();
			Int32 tt = Bios::Clock::GetTicks();
			ss << "|SV:" << EPLPara[0][ii] << "|CACount:" << EPLPara[2][ii] << "|SampleShift:"<< EPLSampleShift[ii] << "|CurrFreq:" << EPLPara[1][ii] << "|EcorrRe:" << EPL_OutVals[0][ii].re << "|EcorrIm:" << EPL_OutVals[0][ii].im << "|PcorrRe:" << EPL_OutVals[1][ii].re << "|PcorrIm:" << EPL_OutVals[1][ii].im \
			<< "|LcorrRe:" << EPL_OutVals[2][ii].re << "|LcorrIm:" << EPL_OutVals[2][ii].im << "|" << std::endl << std::endl;
			LocalParams::Locate().SetLog();
			}

		}*/
			// FPLL NCO adding
//		Complex32 psi;								// FPLL.NCO * exp(1i*NCOStep*HardShift)
//		psi.re = cos(FPLL.NCOStep * HardShift); // int * double
//		psi.im = sin(FPLL.NCOStep * HardShift);
//		FPLL.NCO = IntMath::Normalize(IntMath::Normalize(FPLL.NCO) * IntMath::Normalize(psi)); //
			// end of FPLL adding

		// bit Sync
		if (tv.CurEPLindx > 0)
			tv.BitSync.isFirst = false;
		if (!tv.BitSync.isDone && !tv.BitSync.isFirst)
			DoBitSync();
		// DLL start
		if (((tv.CACounter+1) % tv.DLL.NumIntCA)==((tv.BitSync.CAShift) % tv.DLL.NumIntCA))
		{
			DLLTune();
			if (tv.BitSync.isDone && tv.CACounter > (bits4Sync+CAPerBit))
			{
				tv.CurSNR = estimateSNR();
				if (tv.CurSNR < 30)
					RemoveSv();
			}
			//}
		}
		// FPLL start
		if ((((tv.CACounter+1) % tv.FPLL.NumIntCA)==((tv.BitSync.CAShift) % tv.FPLL.NumIntCA))&&((tv.CACounter+1) > 2*tv.FPLL.NumIntCA)) // *2 добавил
			FPLLTune();
		// change states handling
		//if (tv.BitSync.isDone)
		//	ChangeState();
		//if ((tv.CurEPLindx+1) % tau_upd == 0)
			//if (tv.CurSNR < 30)
			//	RemoveSv();

			//----------------------------------------------------------------
		// can use for debug messages or display some data
		if (((((tv.CACounter+1) % tv.FPLL.NumIntCA)==((tv.BitSync.CAShift) % tv.FPLL.NumIntCA))&&((tv.CACounter+1) > tv.FPLL.NumIntCA))||(((tv.CACounter+1) % tv.DLL.NumIntCA)==((tv.BitSync.CAShift) % tv.DLL.NumIntCA)))
		{
			if (tv.OutputCount < 1000)
			{
				Bool isneed = false;
				if (tv.BitSync.isDone && !isneed)
				{
				// output
					for (Int ii = 0; ii < CAPerBit; ii++)
					{
						std::stringstream& ss = LocalParams::Locate().GetSS();
						Int32 tt = Bios::Clock::GetTicks();
						ss << "|SV:" << index << "|BitCor:" << tv.BitSync.Cor[ii]  << "|" << std::endl << std::endl;
						LocalParams::Locate().SetLog();

					}
					isneed = true;
				}
				/*std::stringstream& ss = LocalParams::Locate().GetSS();
				Int32 tt = Bios::Clock::GetTicks();
				FPLLFilter& fpll = FPLLFilts[item.corr];
				ss << "|SV:" << index << "|CACount:" << tv.CACounter << "|CurrFreq:" << tv.CurrDopplerFreq << "|DLL.Discr:" << tv.DLL.Discr \
				<< "|FPLL.Discrs:" << tv.FPLL.FLLDiscr << "|PLL.Discr:" << tv.FPLL.PLLDiscrs[tv.CACounter % 100] << "|HardShift:" \
				<< tv.HardShift << "|CurSNR:" << tv.CurSNR << "|SampleShift:"<< tv.DLL.SampleShift \
				<< "|EcorrRe:" << tv.EPLCorVals[tv.CurEPLindx][0].re << "|EcorrIm:" << tv.EPLCorVals[tv.CurEPLindx][0].im << "|PcorrRe:" << tv.EPLCorVals[tv.CurEPLindx][1].re << "|PcorrIm:" << tv.EPLCorVals[tv.CurEPLindx][1].im \
				<< "|LcorrRe:" << tv.EPLCorVals[tv.CurEPLindx][2].re << "|LcorrIm:" << tv.EPLCorVals[tv.CurEPLindx][2].im << "|AccelAcc:" << fpll.AccelAcc << "|DLLNumIntCA:" << tv.DLL.NumIntCA << "|FPLLNumIntCA:" << tv.FPLL.NumIntCA \
				<< "|FPLLStateVal:" << tv.FPLL.StateVal << "|" << std::endl << std::endl; //"|DLL.NCOStep:" << tv.DLL.NCOStep << "|FPLL.NCOStep:" << tv.FPLL.NCOStep << std::endl;
				LocalParams::Locate().SetLog();
				tv.OutputCount++;*/
			}
			//if (tv.CurrDopplerFreq == tv.PrevDopplerFreq)
			//	tv.BadSvCount++;
			//else
			//	tv.BadSvCount = 0;
		}

		//if ((tv.BadSvCount == 100)||IntMath::Abs(tv.CurrDopplerFreq)>8000)
		//	RemoveSv();


		tv.CACounter++;
		}
			//-- end of adding */
		UpdateAmplitude(); // for amplitude levels

//		if (flag >= tuner_upd) Demodulator(); // после tuner

//		UpdateIq();
//		UpdateConvolution();

		if(satellite.GetState() < Gnss::Satellite::found){
			Int32 debug_corr = items.find(index)->second.corr;
			continue; // ¬ыкинули в UpdateConvolution
		}

		Bool up;
		if ((flag & 0xF)  == found_one_bit_edge) // ?
			up = (((count - satellite.GetBitEdge(0)) % tau_upd) == 0) && (items.count(index) != 0); // ?
		else
			up = (((count - satellite.GetBitPosition()) % 5) == 0) && (items.count(index) != 0); // ?
		if (count == satellite.GetBitEdge(0)) up = FALSE;
		//if (up) UpdateSatellite();
	}

	// for free corr update ampl too

	for (Int i = 0; i < corrN; ++i) { // ?
		// find free correlator
		Bool busy = FALSE;
		for (ItemsIterator it = items.begin(); it != items.end(); ++it) {
			Item& item = it->second;
			if (i == item.corr) {
				busy = TRUE;
				break;
			}

		}
		if (busy) continue;
		corr = i;
		UpdateAmplitude();
	}

//	led.Off();
}

Void Tracker::DoBitSync()
{
	Item& item = items[index];
	TrackVars& tv = trackvars[item.corr];
	if ((tv.BitSync.PsCounter != B4Stmp))
	{
		tv.BitSync.Ps[tv.BitSync.PsCounter % CAPerBit] += IntMath::Normalize(IntMath::Normalize(tv.EPLCorVals[tv.CurEPLindx][1]) * IntMath::Normalize(~tv.EPLCorVals[tv.CurEPLindx-1][1]));
		tv.BitSync.PsCounter++;
	}
	else
	{
		// first count phase shifts
//		for (UShort ii = 0; ii < (B4Stmp); ii++)				// phase difference among P samples
//			BSBuf[ii] = IntMath::Normalize(IntMath::Normalize(tv.BitSync.Ps[ii+1]) * IntMath::Normalize(~tv.BitSync.Ps[ii]));
		for (UShort ii = 0; ii < CAPerBit; ii++)			//  –асчЄт коррел€ции
		{
//			for (UShort jj = 0; jj < CAPerBit; jj++)
//			{
//				BitSyncCor[ii] += BSBuf[jj*NBits4Sync+ii]; // BitSync.Cor = abs(sum(reshape(Buf, CAPerBit, NBits4Sync).'));
//			}
			tv.BitSync.Cor[ii] = IntMath::Abs(tv.BitSync.Ps[ii]);
		}

		//find the minimum pos
		Int BitSyncCorMin = tv.BitSync.Cor[0];
		UShort SyncPos = 0;
		for (UShort ii = 1; ii < CAPerBit; ii++)
		{
			if (tv.BitSync.Cor[ii] < BitSyncCorMin)
			{
				SyncPos = ii;
				BitSyncCorMin = tv.BitSync.Cor[ii];

			}
		}
		tv.BitSync.CAShift = SyncPos % CAPerBit; //+1
		//satellite.SetBitEdge(SyncPos,)
		tv.BitSync.isDone = true;
		tv.DLL.PosCAStateChanged = tv.CACounter;
		tv.FPLL.PosCAStateChanged = tv.CACounter;
	}
}

Void Tracker::DLLTune()
{
	Item& item = items[index];
	TrackVars& tv = trackvars[item.corr];
	Gnss::Satellite& satellite = satellites[index];
	Complex32 Etmp = 0,Ltmp = 0;
	Int E, L;
	const Int center = (corrL >> 1);

	for (UShort ii = 0; ii < tv.DLL.NumIntCA; ii++)
	{
		Etmp += tv.EPLCorVals[(tv.CACounter - ii) % 40][0];
		Ltmp += tv.EPLCorVals[(tv.CACounter - ii) % 40][2];
	}
	E = IntMath::Abs(Etmp);
	L = IntMath::Abs(Ltmp);
	tv.DLL.Discr = 0.5 * (E - L) / (E + L);
	tv.DLL.NCOStep = -TCA * DLLFilts[item.corr].Step(tv.DLL.Discr);

	// DLL NCO adding
	tv.fd = tv.FPLL.NCOStep * signalLength / (2*pi*TCA); //может заменить nco step на разницу текущей и предыдущей частот? или велосити разницу например
	tv.Buf = tv.fd * TCA * 2 / 1540;
	tv.DLL.NCO = tv.DLL.NCO + tv.DLL.NCOStep - tv.Buf;
		// end of DLL adding

		//pos update
	tv.HardShift = round(tv.DLL.NCO);
	tv.DLL.NCO = tv.DLL.NCO - tv.HardShift;
	Int pos = satellite.GetPosition();
	pos += tv.HardShift;
	tv.DLL.SampleShift = pos + tv.DLL.NCO;
	if (tv.HardShift != 0)
	{

		Int32 deltaBitPos = 0;
		Int32 oldPos = satellite.GetPosition();
		if((oldPos == 4) && (pos == 3)){ // позици€ fpga 0 -> 2045
			deltaBitPos	= -1;
		}
		else if(((oldPos == 3) && (pos == 4))){ // позици€ fpga 2045 -> 0
			deltaBitPos = 1;
		}
		//Int32 bitEdge = satellite.GetBitEdge(0);
		//satellite.SetBitEdge(bitEdge + deltaBitPos, 0);
		satellite.SetPosition(pos); // позици€ максимума
		if (pos < center)
			pos = pos + signalLength;

	}
	regs->pos[corr] = pos - center;
	regs->sv[corr] 	= Gnss::Satellites::Sv(index) - Gnss::Gps::svFirst;
}

Void Tracker::FPLLTune()
{
	Complex32 Pprev = 0,Pcurr = 0, FLLBuf = 0;
	Float* tmpFiltOut;
	Gnss::Satellite& satellite = satellites[index];
	Item& item = items[index];
	TrackVars& tv = trackvars[item.corr];

	for (UShort ii = 0; ii < tv.FPLL.NumIntCA; ii++)
	{
		Pprev += tv.EPLCorVals[(tv.CACounter - tv.FPLL.NumIntCA - ii) % 40][1];
		Pcurr += tv.EPLCorVals[(tv.CACounter - ii) % 40][1];
	}
	FLLBuf = IntMath::Normalize(IntMath::Normalize(Pcurr) * IntMath::Normalize(~Pprev));
	tv.FPLL.FLLDiscr = std::atan(static_cast<Double>(FLLBuf.im) / static_cast<Double>(FLLBuf.re)) / (TCA*tv.FPLL.NumIntCA);  // возможно вли€ет приведение типов
	//tv.FPLL.FLLDiscr = std::atan((FLLBuf.im) / (FLLBuf.re)) / (TCA*tv.FPLL.NumIntCA);
	tv.FPLL.PLLDiscrs[tv.CACounter % 100] = std::atan(static_cast<Double>(Pcurr.im) / static_cast<Double>(Pcurr.re));
	tmpFiltOut = FPLLFilts[item.corr].Step(tv.FPLL.PLLDiscrs[tv.CACounter % 100],tv.FPLL.FLLDiscr);
	tv.FPLL.NCOStep = -TCA * tmpFiltOut[0] / signalLength; //
	tv.PrevDopplerFreq = tv.CurrDopplerFreq;
	tv.CurrDopplerFreq = round(tmpFiltOut[1] / (2*pi));
	satellite.GetParams().doppler = tv.CurrDopplerFreq;
	regs->doppler[corr] = GetSinCos(tv.CurrDopplerFreq);
}

Void Tracker::ChangeState()
{
	Item& item = items[index];
	TrackVars& tv = trackvars[item.corr];
	tv.FPLL.NumCA2CheckState = tv.FPLL.NumsCA2CheckState[tv.FPLL.State];
	tv.DLL.NumIntCA = 20;
	if ((((tv.CACounter) % tv.FPLL.NumCA2CheckState)==(tv.FPLL.PosCAStateChanged % tv.FPLL.NumCA2CheckState))&&((tv.CACounter) > tv.FPLL.PosCAStateChanged))
	{
		tv.FPLL.isStateChanged = false;
		for (UShort ii = 0; ii < tv.FPLL.NumCA2CheckState; ii++)
		{
			tv.FPLL.StatetmpPhase = tv.FPLL.PLLDiscrs[(tv.CACounter - ii) % 100] / pi;
			tv.FPLL.StatePhase += tv.FPLL.StatetmpPhase * tv.FPLL.StatetmpPhase;
		}
		tv.FPLL.StateVal = std::sqrt(tv.FPLL.StatePhase / tv.FPLL.NumCA2CheckState); // value for making the decision about state change
		if (tv.FPLL.StateVal < tv.FPLL.LoTr[tv.FPLL.State])
		{
			if (tv.FPLL.State < 3)
			{
				tv.FPLL.State++;
				tv.FPLL.isStateChanged = true;
			}
			tv.FPLL.isSync = true;
		}
		else if (tv.FPLL.StateVal > tv.FPLL.HiTr[tv.FPLL.State])
		{
			if (tv.FPLL.State > 0)
			{
				tv.FPLL.State--;
				tv.FPLL.isStateChanged = true;
			}
			tv.FPLL.isSync = false;
		}
		else
			tv.FPLL.isSync = true;

		if (tv.FPLL.isStateChanged)
		{
			tv.DLL.State = tv.FPLL.State;
			tv.FPLL.NumIntCA = tv.FPLL.NumsIntCA[tv.FPLL.State];
			tv.DLL.NumIntCA = tv.DLL.NumsIntCA[tv.DLL.State];
			FPLLFilts[item.corr].ChangeParams(tv.FPLL.FilterBands[tv.FPLL.State], TCA*tv.FPLL.NumIntCA);
			DLLFilts[item.corr].ChangeParams(tv.DLL.FilterBands[tv.DLL.State],TCA*tv.DLL.NumIntCA);
		}
	}
}

Float Tracker::estimateSNR()
{
	Complex32 iq_nb;
	Item& item = items[index];
	TrackVars& tv = trackvars[item.corr];
	Float sum_wb = 0.0, sum_nb = 0.0;
	for(Int ii = 0; ii < tau_bit; ii++)
	{
		iq_nb += tv.EPLCorVals[tv.CurEPLindx-ii][1];
		Float re = tv.EPLCorVals[tv.CurEPLindx-ii][1].re;
		Float im = tv.EPLCorVals[tv.CurEPLindx-ii][1].im;

		sum_wb += (re*re + im*im);
	}
	Float re = iq_nb.re;
	Float im = iq_nb.im;
	sum_nb = (re*re + im*im);

	Float shiftedSumNb = (snr_mpy * sum_nb);
	Int updValue = shiftedSumNb/sum_wb;

	if (tv.isFirst)
	{
		tv.snr.Set(updValue);
		tv.isFirst = false;
		return 9999;
	}
	else
	{
		Int snr_int = tv.snr.Update(updValue);
		Float temp = (snr_int - snr_mpy) / (tau_bit * snr_mpy - snr_int);
		Float snr_dBHz = 30 + 10*std::log10(temp);
		return snr_dBHz;
	}
}

Void Tracker::AddSv()
{
	Int i;

	if( (skipSv >> index) & 0x1){
		satellites[index].SetState(Gnss::Satellite::visible);
		return;		// bad sv
	}

	if (items.count(index) != 0) return; // if satellite is already on the tracking

//	std::cout << "add: sv = " << sv << std::endl;
	Bool found = FALSE;

	for (i = 0; i < corrN; ++i) // find free correlator
	{
		Bool busy = FALSE;
		for (ItemsIterator it = items.begin(); it != items.end(); ++it) {
			Item& item = it->second;
			if (i == item.corr) { // ?
				busy = TRUE;
				break;
			}

		}
		if (busy) continue;
		found = TRUE;
		Item item;
		item.corr = i;
		item.skipCount = 0;
		item.iq01.Setup(tauIq, 0);
		item.iq02.Setup(tauIq, 0);
			// added by LT
		TrackVars& trvars = trackvars[item.corr];
		DLLFilter dll(trvars.DLL.FilterOrder, trvars.DLL.FilterBands[trvars.DLL.State], TCA*trvars.DLL.NumIntCA, 0);
		FPLLFilter fpll(trvars.FPLL.FilterOrder[0], trvars.FPLL.FilterOrder[1], trvars.FPLL.FilterBands[trvars.FPLL.State][0], trvars.FPLL.FilterBands[trvars.FPLL.State][1],TCA * trvars.FPLL.NumIntCA, 0, 0);
		DLLFilts[item.corr] = dll;
		FPLLFilts[item.corr] = fpll;
		//DLLFilts.insert(std::make_pair(index,dll));
		//FPLLFilts.insert(std::make_pair(index,fpll));
		//trackvars.insert(std::make_pair(index,trvars));
			//end of adding
		items.insert(std::make_pair(index, item));
		break;
	}

	if (!found){
		satellites[index].SetState(Gnss::Satellite::visible);
		return;		///state
	}

	Gnss::Satellite& satellite = satellites[index];
	Item& item = items[index];
	TrackVars& tv = trackvars[item.corr];

	corr = item.corr;
	satellite.SetCorr(corr);

	Int32 pos = satellite.GetPosition();

	const Int center = corrL >> 1;
	if (pos < center)
		pos = pos + signalLength - center;
	else
		pos = pos - center;

	Int freq = satellite.GetParams().doppler;
	// added by LT
	tv.CurrDopplerFreq = freq;
	// end of adding
	UInt32 sincos = GetSinCos(freq);

	regs->doppler[corr] = sincos; // initial NCO conditions
	regs->pos[corr] = pos;
	regs->sv[corr] 	= Gnss::Satellites::Sv(index) - Gnss::Gps::svFirst;

	satellite.GetParams().flag = tracker_add;
	satellite.GetParams().cn0 = 0; //

	satellite.GetDebugParams().trackerCnt++; //

	// added by LT
	tv.FPLL.NCOStep = 2 * pi * freq / Fs;
	//FPLLFilts[item.corr].ChangeParams(freq*2*pi); // ?? why is minus 1 ?
	// end of adding
//	std::cout << "add_sv:" << sv << "; doppler: " << freq << std::endl;
}

Void Tracker::RemoveSv() //ok
{
	if (items.count(index) != 0) {
		Item& item = items[index];
		trackvars[item.corr] = TrackVars();
		DLLFilts[item.corr] = DLLFilter();
		FPLLFilts[item.corr] = FPLLFilter();
		items.erase(index);
		// added by LT
		//trackvars.erase(index);
		//DLLFilts.erase(index);
		//FPLLFilts.erase(index);
		// end of adding
		for (Int i = 0; i < corrL; ++i) {
			convolution[corr][i].Set(0);
		}

	}
	satellites[index].SetState(Gnss::Satellite::visible);
}

Void Tracker::UpdateAmplitude() //ok
{
	const Int center = (corrL >> 1), step = 3;

	Int a;
	for(Int32 ii = 0; ii < corrV; ii++)
	{
		a = IntMath::Abs(corrData[ii][center - step]);
		amplPtr[ii]->Update(a); // where is declaration?
		a = IntMath::Abs(corrData[ii][center + step]);
		amplPtr[ii]->Update(a);
	}

	Gnss::Antenna& antenna = Gnss::Antenna::Locate();
	antenna.SetPowerGps(amplPtr[0]->Value(), amplPtr[1]->Value(), amplPtr[2]->Value());
}

Void Tracker::UpdateIq()
{
	const Int center = (corrL >> 1);

	rawIq[0] = corrData[0][center]; // ?
	rawIq[1] = corrData[1][center];
	rawIq[2] = corrData[2][center];

	Complex32 z0 = IntMath::Normalize(corrData[0][center]);
	Complex32 z1 = IntMath::Normalize(corrData[1][center]);
	Complex32 z2 = IntMath::Normalize(corrData[2][center]);

	Complex32 iq01 = items[index].iq01.Update(IntMath::Normalize(z1 * ~z0)); //
	Complex32 iq02 = items[index].iq02.Update(IntMath::Normalize(z2 * ~z0));

	satellites[index].SetIq(iq01, iq02);
}

Void Tracker::UpdateConvolution()
{
	#pragma DATA_ALIGN(8)
	static Int32 envelope[corrL];
	const Int center = (corrL >> 1);

	items[index].amplitude.Update(IntMath::Abs(corrData[0][center]));
//	satellites[index].GetDebugParams().updConvol = items[index].amplitude.Value();
	satellites[index].GetDebugParams().updConvol++;


	if ((satellites[index].GetParams().flag & 0xF) == found_one_bit_edge)
		UpdConvolNew(corrData[0], envelope);
	else
		UpdConvolOld(corrData[0], envelope); // old work
}

Void Tracker::UpdConvolNew(Complex32* source, Int32* envelope)
{
	Item& item = items[index];
	Int deltaCount = count - satellites[index].GetBitEdge(0);

	if (deltaCount == 0) {	// clear for new work
		item.badCount0 = 0;
		for (Int i = 0; i < corrL; ++i)	{
			convolution[corr][i].Set(0);
			convolution[corr][i].Setup(tauConvol);
			abs_for_cn0[corr] = 0;

		}
		return;
	}

	for (Int i = 0; i < corrL; ++i){
		updConvol[corr][i] += source[i];		// суммируем 20 раз по 9 фаз
	}
//------------------------- Cуммируем мощности дл€ Pw -----------------------------------------

	Float re = source[corrL >> 1].re, im = source[corrL >> 1].im;
	abs_for_cn0[corr] += (re*re + im*im);

//---------------------------------------------------------------------------------------------

	if ((deltaCount % tau_upd) == 0) { 			// обновление раз в 20 мс
		IntMath::Envelope(updConvol[corr], envelope, corrL);
		IntMath::Peak peak = IntMath::GetPeak(envelope, corrL);

//--------------------------- ќбновл€ем cn0 ------------------------------------------

		re = updConvol[corr][corrL >> 1].re;
		im = updConvol[corr][corrL >> 1].im;
		Float Pn = re*re + im*im;

		Float Pnm = Pn/abs_for_cn0[corr];
		item.cn0.Update(Pnm * 10000);
		abs_for_cn0[corr] = 0;
		Int32 cn0 = item.cn0.Value(); // E(Pnw) * 10000

		Gnss::Satellite& satellite = satellites[index];
		Gnss::Satellite::Params& params = satellite.GetParams();

		params.cn0 = ((cn0 - 10000) << 12)/(200000 - cn0);

//-------------------------------------------------------------------------------------

		if (peak.quality > threshQual0) { 		// если пик 20ки проходит

			for (Int i = 0; i < corrL; ++i){
				convolution[corr][i].Update(updConvol[corr][i] * bit[0]);
				updConvol[corr][i] = 0;
			}
		}
		else {
			item.badCount0 += 20;
			satellites[index].GetDebugParams().badCount0 += 20;
			if (item.badCount0 > badMax0) {
				RemoveSv();
			}
		}
	}
}

Void Tracker::UpdConvolOld(Complex32* source, Int32* envelope)
{
	Item& item = items[index];

	Gnss::Satellite& satellite = satellites[index];
	Gnss::Satellite::Params& params = satellite.GetParams();

// усреднить, а потом уже пороги?

	IntMath::Envelope(source, envelope, corrL);
	IntMath::Peak peak = IntMath::GetPeak(envelope, corrL);
	const Gnss::Drone::Params& paramsGPS = Gnss::Drone::Locate().GetParams();

	if (peak.quality > threshQual0) {

		for (Int i = 0; i < corrL; ++i) {
			convolution[corr][i].Update(source[i]);
		}

		item.badCount0 = 0;
	}
	else{
		satellites[index].GetDebugParams().badCount0++;
		if (++item.badCount0 > badMax0) {
			RemoveSv();

#if DEBUG & DEBUG2
		std::cout << "-- SV " << sv << ": badCount0, quality = " << peak.quality << std::endl;
#endif

		}
	}
}


Void Tracker::UpdateSatellite()
{
	#pragma DATA_ALIGN(8)
	static Complex32 convol[corrL];
	static Int32 envelope[corrL];

	Gnss::Satellite& satellite = satellites[index];
	Item& item = items[index];

	if (count == satellite.GetBitEdge(0)) return; // default 0 ??

	for (Int i = 0; i < corrL; ++i) {
		convol[i] = convolution[corr][i].Value();
	}

	IntMath::Envelope(convol, envelope, corrL);

	peak = IntMath::GetPeak(envelope, corrL);


	Gnss::Satellite::State state = satellite.GetState();
	Gnss::Satellite::Params& params = satellite.GetParams();
	const Gnss::Drone::Params& paramsGPS = Gnss::Drone::Locate().GetParams();
//	info.time = params.tGps;
//	info.latitude = params.latitude;

	Double el = params.elevation.Degrees();
	if( el < (double)elMin){
//		std::cout << "time: " << paramsGPS.tGps <<  " remove 10.0: sv " << sv << " corr " << corr << std::endl;
		RemoveSv();
		return;
	}

	if( (skipSv >> index) & 0x1){
		RemoveSv();
		return;		// bad sv
	}


	if (state == Gnss::Satellite::found) { // first update

		item.skipCount ++;
		if(item.skipCount == 20){
			satellite.SetState(Gnss::Satellite::tracked);
			item.quality = peak.quality;
			item.skipCount = 0;		// кто-то ставит ещЄ статус found
		}
		Tune();
	}
	else if (state == Gnss::Satellite::tracked) { // normal tracking
		if (peak.quality > threshQual1) {
			item.quality = peak.quality;
			item.badCount1 = 0;
			Tune();
		}
		else if (++item.badCount1 > badMax1) {
			satellite.GetDebugParams().badCount1++;
			RemoveSv();

#if DEBUG & DEBUG2
			std::cout << "-- SV " << sv << ": badCount1, quality = " << peak.quality << std::endl;
#endif

		}
	}
}



Void Tracker::Tune()
{
	Gnss::Satellite& satellite = satellites[index];
	const Int center = corrL >> 1;


	Int delta = peak.pos - center;
	if (delta < 0)
		delta = -1;
	else if (delta > 0)
		delta = 1;
	Int pos = satellite.GetPosition() + delta;


	Int32 deltaBitPos = 0;
	Int32 oldPos = satellite.GetPosition();
	if((oldPos == 4) && (pos == 3)){ // позици€ fpga 0 -> 2045
		deltaBitPos	= -1;
	}
	else if(((oldPos == 3) && (pos == 4))){ // позици€ fpga 2045 -> 0
		deltaBitPos = 1;
	}
	Int32 bitEdge = satellite.GetBitEdge(0);
	satellite.SetBitEdge(bitEdge + deltaBitPos, 0);
//----------------------------------------------------------------


	if (pos < 0) {
		pos += signalLength;
	}
	else if (pos >= signalLength) {
		pos -= signalLength;
	}

	satellite.SetPosition(pos); // позици€ максимумв

//	Int32 deltaPosBit = 0;

	if (pos < center)
		pos = pos + signalLength - center;
	else
		pos = pos - center;

	Int freq = satellite.GetParams().doppler;
	UInt32 sincos = GetSinCos(freq);
	regs->pos[corr] = pos;
	regs->doppler[corr] = sincos;
}


Void Tracker::Demodulator() // ? PLL FLL ?
{
	const Int center = (corrL >> 1);

	Complex32 delta[channel], z[channel];
	Complex32 twiddleFreq, complPhase;
	Int32 phase;
	IntMath::Twiddle& twiddle = IntMath::Twiddle::Locate(); //  -2^31..2^31-1  <-->  complex (-pi..pi)
	Item& item = items[index];
	Gnss::Satellite::Params& params = satellites[index].GetParams();

//	for (Int i = 0; i < 1; i++){
	for (Int i = 0; i < corrV; i++)
	{
		z[i] = IntMath::Normalize(corrData[i][center]);
		Demod& dem = item.dmd[i];

		if ((item.flag & (1 << i)) == 0) {
			dem.phase = z[i];
			item.flag |= (1 << i);	// add for demod
		}

		delta[i] = IntMath::Normalize(z[i] * ~dem.phase);
		if (delta[i] == 0) {
//			std::cout << "error_delta. corr: " << corr << std::endl;
			delta[i] = 1;
		}

		phase = delta[i].re * delta[i].im; 	// rad * 2^30

//		if (i == 0) { // freq for main corr
//			item.freq += (phase >> (15 + tauFreq)); 					// rad * 2^15 >> tauFreq / 1 ms
//		}

		dem.freq += (phase >> (15 + tauFreq)); 					// rad * 2^15 >> tauFreq / 1 ms

		complPhase = IntMath::Normalize(twiddle[((phase >> (3 + tauPhase)) * 5) + ((dem.freq * 163) << 7)]);
		dem.phase = IntMath::Normalize(complPhase * dem.phase);		// полное значение фазы отстройки на
 																	// текущий период
	}

	if (item.count++ == 500) {
		Int tempFreq = (item.dmd[0].freq * 159) >> 15; // Hz (1000 / (2 * pi))
		params.doppler += tempFreq;

//		std::cout << "delta: " << tempFreq << std::endl;

		if (params.flag < demod_upd) params.flag = demod_upd;

		Int freq = params.doppler;
		UInt32 sincos = GetSinCos(freq);
		//regs->doppler[corr] = sincos;

		item.dmd[0].freq -= (tempFreq * 206);
		item.dmd[1].freq -= (tempFreq * 206);
		item.dmd[2].freq -= (tempFreq * 206);

		item.count = 0;
	}


	if (params.flag >= demod_upd) { // если подстроили допплер
		for (Int i = 0; i < 1; i++) {
			if ((params.flag & (8 << i)) == 0) Finder(delta[i], i);
			if (((params.flag >> (3 + i)) & 1) == 1) GetBit(delta[i], i);
		}
	}


}


Void Tracker::Finder(Complex32 phase, Int chan)
{
	Gnss::Satellite& satellite = satellites[index];
	Gnss::Satellite::Params& params = satellite.GetParams();

	Item& item = items[index];
	Demod& dem = item.dmd[chan];

	if (dem.counter == 0) dem.bitZnak = phase.re; // если ничего не насчитали еще

	if (dem.bitSkip == 0) { // до первого перескока фазы
		if ((phase.re * dem.bitZnak) > 0) { // если одного знака
			dem.counter++;
		}
		else {
			dem.bitCount = (dem.counter/tau_bit);
			dem.bitSkip++;
			dem.counter = 1;
			if (dem.bitCount > 2) dem.bitCount = 2;
		}
	}

	if (dem.bitSkip != 0) { // был перескок фазы, примерно знаем границу
		if ((phase.re * dem.bitZnak) > 0) { // если одного знака
			dem.counter++;
		}
		else {
			dem.bitCount = 0;
			dem.bitZnak = phase.re;
			dem.counter = 1;
		}

		if (dem.counter == tau_bit) {
			dem.counter = 0;
			dem.bitCount++;
		}

		if (dem.bitCount == 6) {
			dem.bitCount = 0;
			dem.counter = 0;
			satellite.SetBitEdge(count, chan);
			params.flag |= (8 << chan); 			// граница бита найдена
		}
	}


	if (params.flag == found_one_bit_edge) {
		item.count -= (item.count % tau_bit); // обновл€ть допплер на границе бита
		satellite.SetBitPosition(count % 20); // при потере спутника знаем примерно границу, чтобы лучше следить
	}

}

Void Tracker::GetBit(Complex32 phase, Int chan)
{
	Item& item = items[index];
	Demod& dem = item.dmd[chan];
	Gnss::Satellite& satellite = satellites[index];
	Gnss::Satellite::Params& params = satellites[index].GetParams();
	Int delta = count - satellite.GetBitEdge(chan);

	if (delta <= 0) return;

	dem.sum += phase;

	if ((delta % tau_upd) == 0) { // определение бита в tau_upd

		if (dem.sum.re > 0)
			bit[chan] =  1;
		else
			bit[chan] =  -1;
// ----------------------------------------------------------------

/*		Int pos = (delta/tau_bit) - 1; // номер бита с момента определени€ границы
		Int start = corr * corrSize + chan * chanSize; // начало блока данных из 32 бит дл€ каждого канала
		parseData[start + (pos & chanMask)] = bit[chan]; // 1st corr (ch0, ch1, ch2) 2nd corr..

		if (((pos & sizeMask) == sizeMask) && (chan == 0)) { // набрали 8 бит
			ParseDataMail* parseMail = static_cast<ParseDataMail*>(parseBox.Allocate());

			if (parseMail != NULL) {
				parseMail->address = parseData + start + ((pos >> 3) & parseMask) * size ;
				parseMail->count = pos - sizeMask;
				parseMail->sv = sv;
				parseMail->channel = chan;
				parseBox.Post(parseMail);
			}
		}
*/

// -------------------------------------------------------------------

// ------------------------ error -------------------------------------------------------------------------
//		if (dem.sum.re == 0) std::cout << "error_GetBit(); sv = ;" << sv << std::endl;
// ----------------------------------------------------------------------------------------------------------
		dem.sum = 0;
	}
}


#if DEBUG & DEBUG4

Void Tracker::DebugLog()
{
	std::cout << "_______________________________________________________" << std::endl;

	for (ItemsIterator it = items.begin(); it != items.end(); ++it) {
		Int n = it->first;
		Item& item = it->second;
		Gnss::Satellite& satellite = satellites[n];
		const Gnss::Satellite::Params& params = satellite.GetParams();

		Double az = params.azimuth.Degrees();
		if (az < 0) az += 360;
		Double el = params.elevation.Degrees();

		const Double degrees = 180.0 / 3.14159265;
		Double x = item.iq01.Value().re;
		Double y = item.iq01.Value().im;
		Double phi1 = degrees * std::atan2(y, x);

		x = item.iq02.Value().re;
		y = item.iq02.Value().im;
		Double phi2 = degrees * std::atan2(y, x);

		std::cout << "==== SV " << n << " (" << az << ", " << el << ", " << params.doppler
				<< ") position = " << satellite.GetPosition() << ", quality = " << item.quality
				<< ", phi = " << phi1 << " " << phi2 << std::endl;
	}

	std::cout << "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" << std::endl;
}

#else

Void Tracker::DebugLog()
{

}

#endif
