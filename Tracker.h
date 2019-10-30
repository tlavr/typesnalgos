/*
 * Tracker.h
 *
 *  Created on: 24.06.2011
 *      Author: VTV
 */

#ifndef Tracker_H_
#define Tracker_H_
#include <xdc/std.h>

#include "IntMath/Peak.h"
#include "Bios/Handlers.h"
#include "Bios/Mail.h"
#include "Gnss/Satellites.h"
#include "Board/Led.h"
#include "Const.h"
#include "IntMath/RcFilter.h"


// -added by LT

const Float TCA = 0.001; // ca code duration in ms
const Short CAPerBit = 20; // ca codes for one bit
const Short NBits4Sync = 100; // bits for sync
const Int Fs = 2046000;
const Short bits4Sync = CAPerBit * NBits4Sync+1;
const Short B4Stmp = bits4Sync-1;
const Float pi = 3.14159265358979323846264; //pi 3.14159265358979323846264
const Int snr_shift 	= 13; 					// для хранения отношения с нормальной точностью
const Int snr_mpy 	= (1 << snr_shift);

/*struct Track_str{ //struct for tracking containing all the parameters
	//Double SamplesShifts; // == pos + delta
	//Complex32 CorVals; // ==corr
	//Double HardSamplesShifts; // == pos
	//Double FineSamplesShifts; // == delta
	//Double DLL; // DLL tracking log
	//Double FPLL; // FPLL tracking log
};*/

struct BitSync_str{ //struct for BitSync
	//UInt32 CAShifts; // periods of CA to skip for bit beginning
	//Complex32 Cors; // corr values to detect bit sync
	Bool isDone; // bit sync isDone?
	Bool isFirst;
	Complex32 Ps[CAPerBit]; // corr values for bit sync
	UInt PsCounter; // number of corr values already got
	Short CAShift; // bit sync number
	Int Cor[CAPerBit]; // array of corr [CAPerBit]
	BitSync_str(): isDone(false), isFirst(true) {
		for (int ii = 0; ii < CAPerBit; ii++)
			Ps[ii] = 0;
		PsCounter = 0;
		CAShift = 0;
		for (int ii = 0; ii < CAPerBit; ii++)
					Cor[ii] = 0;
	};
};

struct DLL_str{ // Struct for DLL (code tracking)
	Short FilterOrder;
	Float FilterBands[4];
	Short NumsIntCA[4]; // period of integration for filtering
	Short NumsCA2CheckState[4]; // periods of CA code to change the state of tracker
	Float HiTr[4]; // thresholds of changing tracker's state
	Float LoTr[4];
	Float NCO;
	Float NCOStep;
	Float SampleShift;
	Bool isSync;
	Short State;
	Short NumIntCA;
	Int PosCAStateChanged;
	Float Discr;
	DLL_str()
	{
		FilterOrder = 2;
		FilterBands[0] = 5;
		FilterBands[1] = 5;
		FilterBands[2] = 5;
		FilterBands[3] = 5;
		NumsIntCA[0] = 4;
		NumsIntCA[1] = 10;
		NumsIntCA[2] = 20;
		NumsIntCA[3] = 20;
		NumsCA2CheckState[0] = 100;
		NumsCA2CheckState[1] = 100;
		NumsCA2CheckState[2] = 100;
		NumsCA2CheckState[3] = 100;
		HiTr[0] = 0.5;
		HiTr[1] = 0.5;
		HiTr[2] = 0.5;
		HiTr[3] = 0.5;
		LoTr[0] = 0.05;
		LoTr[1] = 0.05;
		LoTr[2] = 0.05;
		LoTr[3] = 0.05;
		SampleShift = 0;
		isSync = false;
		NCO = 0;
		NCOStep = 0;
		State = 3;
		NumIntCA = 20;
		PosCAStateChanged = 0;
		Discr = 0;
	}
};

struct FPLL_str{ // Struct for freq and phase tracking
	Short FilterOrder[2];
	Short FilterBands[4][2];
	Short NumsIntCA[4]; // period of integration for filtering
	Short NumsCA2CheckState[4]; // periods of CA code to change the state of tracker
	Short NumCA2CheckState;
	Float HiTr[4]; // thresholds of changing tracker's state
	Float LoTr[4];
	Complex32 NCO;
	Double NCOStep;
	Bool isSync;
	Bool isStateChanged;
	Short State;
	Short NumIntCA;
	Int PosCAStateChanged;
	Double FLLDiscr;
	Float StatePhase;
	Float StateVal;
	Float StatetmpPhase;
	Double PLLDiscrs[100];
	FPLL_str()
	{
		FilterOrder[0] = 2;
		FilterOrder[1] = 3;
		FilterBands[0][0] = 5;
		FilterBands[0][1] = 5;
		FilterBands[1][0] = 5;
		FilterBands[1][1] = 5;
		FilterBands[2][0] = 5;
		FilterBands[2][1] = 5;
		FilterBands[3][0] = 5;
		FilterBands[3][1] = 5;
		NumsIntCA[0] = 4;
		NumsIntCA[1] = 10;
		NumsIntCA[2] = 20;
		NumsIntCA[3] = 20;
		NumsCA2CheckState[0] = 100;
		NumsCA2CheckState[1] = 100;
		NumsCA2CheckState[2] = 100;
		NumsCA2CheckState[3] = 100;
		HiTr[0] = 0.5;
		HiTr[1] = 0.5;
		HiTr[2] = 0.5;
		HiTr[3] = 0.5;
		LoTr[0] = 0.05;
		LoTr[1] = 0.05;
		LoTr[2] = 0.05;
		LoTr[3] = 0.05;
		isSync = false;
		isStateChanged = false;
		NCO = 1;
		NCOStep = 0;
		State = 3;
		NumIntCA = 20;
		PosCAStateChanged = 0;
		FLLDiscr = 0;
		StatePhase = 0;
		StateVal = 0;
		StatetmpPhase = 0;
		NumCA2CheckState = NumsCA2CheckState[State];
		for (int ii = 0; ii < 20; ii++)
			PLLDiscrs[ii] = 0;

	}
};
// --- end of adding */

class Tracker: public Bios::ControlledHandler {
public:
	struct Params {
		Int32 tauIq;
		Int32 tauConvol;
		Int32 threshQual0;
		Int32 threshQual1;
		Int32 badMax0;
		Int32 badMax1;
		UInt32 skipSv;
		Int32	elMin;
	};

	Tracker(Bios::Mailbox& dataBox, Bios::Mailbox& controlBox, Bios::Mailbox& demodBox);

	Params GetParams();
	Void SetParams(const Params& params);
	Void SetMode(const Int setMode);

protected:
	virtual Void Prolog();
	virtual Void Control(Bios::Mail* mail);
	virtual Void Process(Bios::Mail* mail);

	Void AddSv();
	Void RemoveSv();
	Void UpdateAmplitude();
	Void UpdateIq();
	Void UpdateConvolution();
	Void UpdateSatellite();
	Void Tune();

	// added by LT
	Void DoBitSync();
	Void DLLTune();
	Void FPLLTune();
	Void ChangeState();
	Float estimateSNR();
	// end of adding

	Void Demodulator();
	Void Finder(Complex32 phase, Int chan);
	Void GetBit(Complex32 phase, Int chan);
	Void UpdConvolOld(Complex32* source, Int32* envelope);
	Void UpdConvolNew(Complex32* source, Int32* envelope);

	Void DebugLog();

private:
	Gnss::Satellites& satellites;
	Complex32* address;
	UInt32 count;
	Int index; // index of the satellite
	Int corr;
	IntMath::Peak peak;
	Board::Led& led;

	Bios::Mailbox& demodBox;
	Int bit[3];
	Int graph;
	Int mode;

	Complex32 corrData[corrV][corrL];
};


//------- added by LT
class DLLFilter{
public:
	DLLFilter() {}
	DLLFilter(Short c_Order, Short c_Bnd, Float c_T, Float c_VelocAcc)
	{
		Double w0;
		Order = c_Order;
		Bnd = c_Bnd;
		T = c_T;
		VelocAcc = c_VelocAcc;
		CalcCoeffs();
		result = 0;
	}
	Float Step(Float PhaseErInput);
	void ChangeParams(UShort Bn, Float c_T)
	{
		Bnd = Bn;
		T = c_T;
		CalcCoeffs();
	}

protected:
	UShort Order;
	UShort Bnd;
	Float T;
	Float VelocAcc;
	Float CoefDLL1;
	Float CoefDLL2;
	Float result;

	void CalcCoeffs()
	{
		Float w0;
		w0 = Bnd / 0.53;
		CoefDLL1 = w0*w0;
		CoefDLL2 = w0*1.414;
	}
};

inline Float DLLFilter::Step(Float PhaseErInput)
{
	result = PhaseErInput * CoefDLL1 * T * 0.5 + PhaseErInput * CoefDLL2 + VelocAcc;
	VelocAcc += PhaseErInput * CoefDLL1 * T;
	return result;
}

class FPLLFilter{
public:
	Float AccelAcc;
	FPLLFilter() {}
	FPLLFilter(Short c_Order0,Short c_Order1, Short c_Bnd0, Short c_Bnd1, Float c_T, Float c_VelocAcc, Float c_AccelAcc)
	{
		Float w0, w1;
		Order[0] = c_Order0;
		Order[1] = c_Order1;
		Bnf = c_Bnd0;
		Bnp = c_Bnd1;
		T = c_T;
		VelocAcc = c_VelocAcc;
		AccelAcc = c_AccelAcc;
		w0 = Bnf / 0.53;
		CoefFLL1 = w0*w0;
		CoefFLL2 = 1.414*w0;
		w1 = Bnp / 0.7845;
		CoefPLL1 = w1*w1*w1;
		CoefPLL2 = 1.1 * w1*w1;
		CoefPLL3 = 2.4 * w1;
		result = 0;
		output[0] = 0;
		output[1] = 0;
	}
	Float* Step(Float PhaseErInput, Float FreqErInput);
	void ChangeParams(Short* Bn, Float c_T)
	{
		Bnf = Bn[0];
		Bnp = Bn[1];
		T = c_T;
		CalcCoefs();
	}
	void ChangeParams(Float c_VelocAcc)
	{
		VelocAcc = c_VelocAcc;
	}

protected:
	UShort Order[2];
	UShort Bnf;
	UShort Bnp;
	Float T;
	Float VelocAcc;
	Float CoefFLL1;
	Float CoefFLL2;
	Float CoefPLL1;
	Float CoefPLL2;
	Float CoefPLL3;
	Float result;
	Float output[2];
	void CalcCoefs()
	{
		Float w0, w1;
		w0 = Bnf / 0.53;
		CoefFLL1 = w0*w0;
		CoefFLL2 = 1.414*w0;
		w1 = Bnp / 0.7845;
		CoefPLL1 = w1*w1*w1;
		CoefPLL2 = 1.1 * w1*w1;
		CoefPLL3 = 2.4 * w1;
	}

};

inline Float* FPLLFilter::Step(Float PhaseErInput, Float FreqErInput)
{
	result = FreqErInput * CoefFLL2 * T * 0.5 + FreqErInput * CoefFLL1 * T * T * 0.25 + PhaseErInput * CoefPLL1 * T * T * 0.25 + PhaseErInput * CoefPLL2 * T * 0.5 + PhaseErInput * CoefPLL3 + AccelAcc * T * 0.25 + VelocAcc*0.5; //veloc*0.5 // accel * 0.25*T
	VelocAcc += FreqErInput * CoefFLL2 * T + FreqErInput * CoefFLL1*T*0.5*T + PhaseErInput*CoefPLL1*T*0.5*T+PhaseErInput*CoefPLL2*T+AccelAcc*T*0.5; //accel * 0.5
	AccelAcc += FreqErInput*CoefFLL1*T + PhaseErInput*CoefPLL1*T;
	output[0] = result;
	output[1] = VelocAcc;
	return output;
}
//*/

class TrackVars{
public:
	// added
	UInt CACounter; // = 0;
	Int CurrDopplerFreq;// = 0;
	Int PrevDopplerFreq;// = 0;
	UShort CurEPLindx;
	Float fd, Buf;
	Short HardShift;
	Short OutputCount;// = 0;
	Short OutputCount_corr;
	Short BadSvCount;// = 0;
	Complex32 EPLCorVals[40][3]; 	 // containing Early, Prompt and Late corrs
	Track_str Track;
	BitSync_str BitSync;
	DLL_str DLL;
	FPLL_str FPLL;
	Bool isFirst;
	Float CurSNR;
	IntMath::RcFilter<Int32> snr; 	// сам фильтр для ОСШ
//	DLLFilter DLLFilt(DLL.FilterOrder, DLL.FilterBands, TCA*DLL.NumIntCA, 0);
//	FPLLFilter FPLLFilt(FPLL.FilterOrder[0], FPLL.FilterOrder[1], FPLL.FilterBands[FPLL.State][0], FPLL.FilterBands[FPLL.State][1],TCA * FPLL.NumIntCA, 0, 0);
	// --- end of adding */
	TrackVars()
	{
		CACounter = 0;
		CurrDopplerFreq = 0;
		CACounter = 0;
		CurrDopplerFreq = 0;
		PrevDopplerFreq = 0;
		CurEPLindx = 0;
		fd = 0;
		Buf = 0;
		isFirst = true;
		HardShift = 0;
		OutputCount = 0;
		OutputCount_corr = 0;
		BadSvCount = 0;
		CurSNR = 0;
		snr.Setup(5); // 5 соответствует тау_фильтра 1/(2^5), т.е. длина окна 32
		for (int ii = 0; ii < 40; ii++)
			for (int jj = 0; jj < 3; jj++)
				EPLCorVals[ii][jj] = 0;
	}
};

#endif // Tracker_H_
