#FPS/APM Counter v5.2 Made by Ninfia
# 0x51CE84 Exactly 1000 Needed
from eudplib import *
import math

fpsoffset = 0x58F450
apmoffset = 0x58F454
peroffset = 0x58F458
cycleoffset = 0x58F45C
qcmax = 0
alert = 1
alertmsg = ""
stackon = 0
stacktest = 0
stackoff1 = 0x58F460
stackoff2 = 0x58F464
stackoff3 = 0x58F468
stackoff4 = 0x58F46C
startlimit = 60
endlimit = 40
stacklimit = 60
stackratio = 0.8
stackopt = 0
debug = 0
turbo = 1
stackalert = 0
for k, v in settings.items():
	if k.lower() == "turbo":
		turbo = int(v)
	if k.lower() == "stack":
		startstr = ""
		endstr = ""
		stackstr = ""
		addstr = ["%", "%", "%"]
		stackon = 1
		stackopt, startlimit, endlimit, stacklimit, stackratio = v.split(",")
		stackopt = int(stackopt)
		if int(startlimit,16) < 0x500000:
			startlimit = int(startlimit)
			stackalert = stackalert + 1
			startstr = "Start : {:d}".format(startlimit)
		else:
			startlimit = int(startlimit,16)
			startstr = "Start : {:X}".format(startlimit)
			if stackopt > 0:
				addstr[0] = ""

		if int(endlimit,16) < 0x500000:
			endlimit = int(endlimit)
			stackalert = stackalert + 1
			endstr = "End : {:d}".format(endlimit)
		else:
			endlimit = int(endlimit,16)
			endstr = "End : {:X}".format(endlimit)
			if stackopt > 0:
				addstr[1] = ""

		if int(stacklimit,16) < 0x500000:
			stacklimit = int(stacklimit)
			stackstr = "Stack : {:d}".format(stacklimit)
		else:
			stacklimit = int(stacklimit,16)
			stackstr = "Stack : {:X}".format(stacklimit)
			if stackopt > 0:
				addstr[2] = ""

		stackratio = float(stackratio)
		if stackratio > 1.0:
			raise EPError("[APMCounter] stack ratio must less or equal than 1.0 (input : %f)." % (stackratio))
		elif stackalert == 2 and startlimit <= endlimit:
			raise EPError("[APMCounter] start limit must larger than end limit (%d%% <= %d%%)." % (startlimit, endlimit)) 
		if stackopt <= 0:
			print("[APMCounter] Stack Counter Enabled → (Number) "+startstr+", "+endstr+", "+stackstr+", Ratio : {:f}".format(stackratio))
		else:
			print("[APMCounter] Stack Counter Enabled → (Percent) "+startstr+addstr[0]+", "+endstr+addstr[1]+", "+stackstr+addstr[2]+", Ratio : {:f}".format(stackratio))
	if k.lower() == "test":
		stacktest = 1
		stackoff1, stackoff2, stackoff3, stackoff4 = v.split(",")
		stackoff1 = int(stackoff1,16)
		stackoff2 = int(stackoff2,16)
		stackoff3 = int(stackoff3,16)
		stackoff4 = int(stackoff4,16)
		print("[APMCounter] Stack Output Enabled → Switch : {:X}, Avg : {:X}, Count : {:X}, Exp Avg : {:X}".format(stackoff1, stackoff2, stackoff3, stackoff4))
	if k.lower() == "debug":
		debug = int(v)
		print("[APMCounter] Debug Mode Enabled → Input : {:d}".format(debug))
	if k.lower() == "output":
		fpsoffset, apmoffset, peroffset, cycleoffset = v.split(",")
		fpsoffset = int(fpsoffset,16)
		apmoffset = int(apmoffset,16)
		peroffset = int(peroffset,16)
		cycleoffset = int(cycleoffset,16)
	if k.lower() == "alert":
		alert = int(v)
	if k.lower() == "qcmax":
		qcmax = int(v)
	if alert == 0:
		alertmsg = "Off"
	else:
		alertmsg = "On"
if turbo > 0:
	print("[APMCounter] Output → EUDTurbo | FPS : 0x{:X}, APM : 0x{:X}, APM(%) : 0x{:X}, Cycle : 0x{:X}, QCUnit Max : {:d}, Alert {}".format(fpsoffset, apmoffset, peroffset, cycleoffset, qcmax, alertmsg))
else:
	print("[APMCounter] Output → No EUDTurbo | FPS : 0x{:X}, APM : 0x{:X}, APM(%) : 0x{:X}, Cycle : 0x{:X}, QCUnit Max : {:d}, Alert {}".format(fpsoffset, apmoffset, peroffset, cycleoffset, qcmax, alertmsg))

if debug > 0:
	Chk = Db(0x100)
	Chkepd, Chkptr, CC = EUDCreateVariables(3)
Void = Db(0x100)
PList = Db(0x400)
PEPD = EPD(PList)
PData = {0x60:12,0x61:13,0x62:5,0x63:0xFF,0x64:0xFF,0x65:0xFF,
	0x05:1,0x09:0xFE,0x0A:0xFE,0x0B:0xFE,0x0C:8,0x0D:3,0x0E:5,
	0x13:3,0x14:10,0x15:11,0x18:1,0x19:1,0x1A:2,0x1B:1,0x1C:1,0x1D:1,
	0x1E:2,0x1F:3,0x20:3,0x21:2,0x22:2,0x23:3,0x25:2,0x26:2,0x27:1,
	0x28:2,0x29:3,0x2A:1,0x2B:2,0x2C:2,0x2D:2,0x2E:1,0x2F:5,
	0x30:2,0x31:1,0x32:2,0x33:1,0x34:1,0x35:3,0x36:1,0x55:2,0x58:5,0x5A:1,
	0x12:0xFD,0x0F:0xFD,0x06:0xFD,0x07:0xFD,
	0x08:1,0x10:1,0x11:1,0x37:7,0x48:13,0x49:5,0x54:1,0x56:10,0x57:2
}

Size, KeyA, KeyB, Dummy, Kret, N500, N1000, NFFFF, NE51CE8C, NE51CE84, NLimit, NNum, N63, N126, N240, N7FFFFFFF, N654880, NE654AA0, NE654A70, N64 = EUDCreateVariables(20)
Stack, SNum, SS, EAvg, SLimit, ELimit, ILimit, SRatio = EUDCreateVariables(8)
def CreateKey():
	RawTrigger(actions=[Kret.SetNumber(0)])
	for i in range(32):
		RawTrigger(actions=[SetSwitch(0,Random)])
		RawTrigger(conditions=[Switch(0,Set)],actions=[Kret.AddNumber(2**i)])
	return Kret

def EncValue(Value): #(X+A)^B
	return f_bitxor(Value+KeyA,KeyB)

def DecValue(Value): #
	return f_bitxor(Value,KeyB)-KeyA

def onPluginStart():
	if debug > 0:
		Chkepd << EPD(Chk)
		Chkptr << Chk
		DoActions(SetDeathsX(Chkepd+0x9C//4,SetTo,0x00000000,0,0xFF000000))
	
	BSW = EUDVariable()
	RawTrigger(conditions=[Switch(0,Cleared)],actions=[BSW.SetNumber(0)])
	RawTrigger(conditions=[Switch(0,Set)],actions=[BSW.SetNumber(1)])

	KeyA << CreateKey()
	KeyB << CreateKey()
	Dummy << CreateKey()
	
	NNum << EncValue(2) # Least Stack Count
	NLimit << EncValue(3) # Max PID Level
	N500 << EncValue(500)
	N1000 << EncValue(1000)
	NFFFF << EncValue(0xFFFF)
	NE51CE84 << EncValue(EPD(0x51CE84))
	NE51CE8C << EncValue(EPD(0x51CE8C))
	N7FFFFFFF << EncValue(0x7FFFFFFF)
	N654880 << EncValue(0x654880)
	NE654AA0 << EncValue(EPD(0x654AA0))
	NE654A70 << EncValue(EPD(0x654A70))
	N64 << EncValue(64)
	
	if turbo > 0:
		N240 << EncValue(240)
		N63 << EncValue(63)
		N126 << EncValue(126)
	else:
		N240 << EncValue(120)
		N63 << EncValue(124)
		N126 << EncValue(249)

	if stackon > 0:
		SRatio << EncValue(int(stackratio*10000))
		if stacklimit < 0x500000:
			ILimit << EncValue(stacklimit)
		else:
			ILimit << EncValue(EPD(stacklimit))
		if startlimit < 0x500000:	
			SLimit << EncValue(startlimit)
		else:
			SLimit << EncValue(EPD(startlimit))
		if endlimit < 0x500000:
			ELimit << EncValue(endlimit)
		else:
			ELimit << EncValue(EPD(endlimit))

	Kret << 0
	RawTrigger(conditions=[BSW.Exactly(0)],actions=[SetSwitch(0,Clear)])
	RawTrigger(conditions=[BSW.Exactly(1)],actions=[SetSwitch(0,Set)])

def beforeTriggerExec():
	if alert != 0:
		if EUDIf()((ElapsedTime(AtLeast,1),ElapsedTime(AtMost,2))):
			if EUDIf()((Deaths(DecValue(NE51CE84),AtLeast,DecValue(N1000)+1,0))):
				ActBox = []
				for i in range(8):
					ActBox.append(SetCurrentPlayer(i))
					ActBox.append(DisplayText("\n\n\n\n\n\n\x13\x08[APMCounter] FATAL ERROR : 배속없이 턴레이트 24로 시작해주세요.\n\n\n\n"))
					ActBox.append(PlayWAV("sound\\Misc\\Buzz.wav"))
					ActBox.append(PlayWAV("sound\\Misc\\Buzz.wav"))
					ActBox.append(Defeat())
				DoActions(ActBox)
			EUDEndIf()
		EUDEndIf()

	if EUDExecuteOnce()():
		InitBox = []
		for i in range(0x100):
			if PData.get(i,0) == 0:
				InitBox.append(SetDeaths(PEPD+i,SetTo,0,0))
			else:
				InitBox.append(SetDeaths(PEPD+i,SetTo,PData[i],0))
		DoActions(InitBox)
	EUDEndExecuteOnce()

	APMP = EUDVariable()
	FPS = EUDVariable()
	Check = EUDVariable()
	HCheck = EUDVariable()
	GameTime = EUDVariable()
	RealTime = EUDVariable()
	Δx, Δy, Δt, Δu = EUDCreateVariables(4)
	PID, Count, APM, Loc, SCount, Loop, Sub, TSub, MAX, Num, Cmp0, Cmp1, Cmp2, Cmp3, LocEPD, OrigPID, pPID, Allow, HNum1, HNum2, SRealTime, SGameTime, ppPID, pCheck, ITemp, STemp, ETemp = EUDCreateVariables(27)
	END = Forward()
	HACK = Forward()
	PASS = Forward()
	JUMP = Forward()

	if EUDIf()((ElapsedTime(AtLeast,2))):
		DoActions(SetMemory(cycleoffset,SetTo,0))

		GameTime << DecValue(GameTime)
		SGameTime << DecValue(SGameTime)
		RealTime << DecValue(RealTime)
		SRealTime << DecValue(SRealTime)
		Δu << DecValue(Δu)
		Count << DecValue(Count)
		SCount << DecValue(SCount)
		
		if stackon > 0:
			SS << DecValue(SS)
			Stack << DecValue(Stack)
			SNum << DecValue(SNum)
			EAvg << DecValue(EAvg)
			if stacklimit < 0x500000:
				ITemp << DecValue(ILimit)
			else:
				ITemp << f_maskread_epd(DecValue(ILimit),0xFFFFFFFF)
			if startlimit < 0x500000:	
				STemp << DecValue(SLimit)
			else:
				STemp << f_maskread_epd(DecValue(SLimit),0xFFFFFFFF)
			if endlimit < 0x500000:
				ETemp << DecValue(ELimit)
			else:
				ETemp << f_maskread_epd(DecValue(ELimit),0xFFFFFFFF)

		if EUDExecuteOnce()():
			GameTime << 0
			SGameTime << 0
			RealTime << 0
			SRealTime << 0
			Δu << 0
			Count << 0
			SCount << 0

			if stackon > 0:
				SS << 0
				Stack << 0
				SNum << 0
				EAvg << 0
		EUDEndExecuteOnce()

		Δx = f_maskread_epd(DecValue(NE51CE8C),0xFFFFFFFF)
		Δy << 0xFFFFFFFF - Δx
		Δt << Δy - Δu
		RealTime << RealTime + Δt
		SRealTime << SRealTime + Δt
		RawTrigger(conditions=[Δt.Exactly(0)],actions=[RealTime.AddNumber(1),SRealTime.AddNumber(1)])
		Δu << Δy
		DoActions([GameTime.AddNumber(1),SGameTime.AddNumber(1)])
		RawTrigger(conditions=[Δt.AtLeast(0x80000000)],actions=[HCheck.SetNumber(1)])

		# 1st 0이면 통과
		Loc << DecValue(N654880)+Size
		PID << f_bread(Loc)

		EUDJumpIf((PID == 0), PASS)
		OrigPID << PID

		# 2nd Hack 감지
		DoActions([TSub.SetNumber(0),Loop.SetNumber(0),Allow.SetNumber(DecValue(NLimit)),pPID.SetNumber(0),pCheck.SetNumber(0)])
		Trigger(conditions=[Δt >= DecValue(N63)+1],actions = [Allow.SetNumber(DecValue(NLimit)+1)])

		Trigger(conditions=[OrigPID != 0x13, OrigPID != 0x0],actions=[pCheck.SetNumber(1)])
		if EUDWhile()((Loop < Allow)):
			Sub << f_maskread_epd(PEPD+PID,0xFF)
			if EUDIf()((Sub == 0xFF)): # Select Type 1 
				Num << f_bread(Loc+TSub+1)
				Sub << Num*4+2
			if EUDElseIf()((Sub == 0xFE)): # Select Type 2 
				Num << f_bread(Loc+TSub+1)
				Sub << Num*2+2
			if EUDElseIf()((Sub == 0xFD)): # Invaild Type 
				EUDJump(HACK)
			EUDEndIf()

			EUDJumpIf((Sub.Exactly(0)), JUMP)

			DoActions([TSub.AddNumber(Sub),Loop.AddNumber(1)])
			ppPID << pPID
			pPID << PID
			PID << f_bread(Loc+TSub)

			Trigger(conditions=[PID != 0x13, PID != 0x0],actions=[pCheck.SetNumber(1)])
			RawTrigger(conditions=[PID.Exactly(0x13),pPID.Exactly(0x13)],actions=[Loop.SubtractNumber(1)])
			RawTrigger(conditions=[Loop.Exactly(2),PID.Exactly(0x13),ppPID.Exactly(0x13)],actions=[Allow.AddNumber(1)])
			
			if EUDIf()((Δt <= DecValue(N126), PID == pPID)): 
				EUDJumpIf((EUDOr(PID == 0x60, PID == 0x63), Δt <= DecValue(N63)), HACK)
				EUDJumpIf((PID >= 0x61, PID <= 0x62), HACK)
				EUDJumpIf((PID >= 0x64, PID <= 0x65), HACK)
				EUDJumpIf((PID >= 0x9, PID <= 0xB), HACK)
				EUDJumpIf((PID >= 0x14, PID <= 0x15), HACK)

				EUDJumpIf((Loop.Exactly(2), PID != 0x13, PID == ppPID, Δt <= DecValue(N63)), HACK)
			EUDEndIf()

		EUDEndWhile()

		if EUDIf()((Never())):
			JUMP << RawTrigger(actions=[TSub.SetNumber(0)])
		EUDEndIf()

		if EUDIf()((Δt <= DecValue(N126), TSub > 0)): # Vaild PID
			LocEPD << EPD(Loc+TSub)
			DoActions([SetMemory(Void,SetTo,Loc+TSub)])
			if EUDIf()((MemoryX(Void,Exactly,1,3))):
				Cmp0 << f_maskread_epd(LocEPD,0xFFFFFF00)
			if EUDElseIf()((MemoryX(Void,Exactly,2,3))):
				Cmp0 << f_maskread_epd(LocEPD,0xFFFF0000)
			if EUDElseIf()((MemoryX(Void,Exactly,3,3))):
				Cmp0 << f_maskread_epd(LocEPD,0xFF000000)
			if EUDElse()():
				Cmp0 << f_maskread_epd(LocEPD,0xFFFFFFFF)
			EUDEndIf()				
			Cmp1 << f_maskread_epd(LocEPD+1,0xFFFFFFFF)
			Cmp2 << f_maskread_epd(LocEPD+2,0xFFFFFFFF)
			Cmp3 << f_maskread_epd(LocEPD+3,0xFFFFFFFF)

			EUDJumpIf((EUDOr(Cmp0 > 0, Cmp1 > 0, Cmp2 > 0, Cmp3 > 0)), HACK)
			DoActions([SetMemory(Void,SetTo,0)])
		EUDEndIf()

		# 3rd 매크로 감지 (부대지정 예외)
		EUDJumpIf((pCheck.Exactly(1)), END)
		
		if EUDIf()((Never())):
			END << RawTrigger(actions=[Count.AddNumber(1),SCount.AddNumber(1)])
		if EUDElseIf()((Never())):
			HACK << RawTrigger()
			MAX << FPS//10+1
			DoActions([Count.SetNumber(MAX),SCount.SetNumber(MAX),SetMemoryX(cycleoffset,SetTo,4,4)])

			if debug > 0:
				if EUDIf()((ElapsedTime(AtLeast,10),DeathsX(Chkepd+0x9C//4,Exactly,0x00000000,0,0xFF000000))):	
					for i in range(39):
						DoActions(SetDeaths(Chkepd+i,SetTo,f_maskread_epd(EPD(0x654880+4*i),0xFFFFFFFF),0)) 
					DoActions([CC.SetNumber(1),SetDeathsX(Chkepd+0x9C//4,SetTo,0x01000000,0,0xFF000000)]) 
				EUDEndIf()
		EUDEndIf()
		PASS << RawTrigger()

		if EUDIf()((Check==0,RealTime>=DecValue(N500))):
			FPS << (10000*SGameTime)//SRealTime
			MAX << FPS//10+1
			Trigger(conditions=[HCheck.Exactly(1)],actions=[HCheck.SetNumber(0),FPS.SetNumber(DecValue(NFFFF))])
			APM << SCount+1
			Trigger(conditions=[APM >= MAX],actions=[APM.SetNumber(MAX)])
			APMP << (SCount*1000)//FPS
			if EUDIf()((FPS <= DecValue(N240)-10)):
				MAX << (FPS*100)//DecValue(N240)
				Trigger(conditions=[APMP.AtLeast(MAX)],actions=[APMP.SetNumber(MAX)])
			EUDEndIf()
			Trigger(conditions=[APMP.AtLeast(101)],actions=[APMP.SetNumber(100)])
			if EUDExecuteOnce()():
				FPS << 0
				APM << 0
				APMP << 0
			EUDEndExecuteOnce()

			if stackon > 0:
				if stackopt > 0:
					if EUDIf()((ITemp.AtLeast(1), STemp > ETemp, SS == 0, APMP >= STemp)):
						SS << 1 
					EUDEndIf()

					if EUDIf()((SS == 1)):
						DoActions([SNum.AddNumber(1),Stack.AddNumber(APMP)]) # Stack Avg
						EAvg << (DecValue(SRatio)*APMP + (10000-DecValue(SRatio))*EAvg)//10000 # Calc EXP Avg
					EUDEndIf()

					if EUDIf()((SS == 1, SNum >= DecValue(NNum), EAvg <= ETemp)):
						SS << 0
						if EUDIf()(((Stack//SNum) >= ITemp)):
							DoActions([SetMemoryX(cycleoffset,SetTo,8,8)]) # Signal
						EUDEndIf()
						DoActions([
							SS.SetNumber(0),
							SNum.SetNumber(0),
							Stack.SetNumber(0),
							EAvg.SetNumber(0),
						])
					EUDEndIf()
				else:
					if EUDIf()((ITemp.AtLeast(1), STemp > ETemp, SS == 0, APM >= STemp)):
						SS << 1 
					EUDEndIf()

					if EUDIf()((SS == 1)):
						DoActions([SNum.AddNumber(1),Stack.AddNumber(APM)]) # Stack Avg
						EAvg << (DecValue(SRatio)*APM + (10000-DecValue(SRatio))*EAvg)//10000 # Calc EXP Avg
					EUDEndIf()

					if EUDIf()((SS == 1, SNum >= DecValue(NNum), EAvg <= ETemp)):
						SS << 0
						if EUDIf()(((Stack//SNum) >= ITemp)):
							DoActions([SetMemoryX(cycleoffset,SetTo,8,8)]) # Signal
						EUDEndIf()
						DoActions([
							SS.SetNumber(0),
							SNum.SetNumber(0),
							Stack.SetNumber(0),
							EAvg.SetNumber(0),
						])
					EUDEndIf()

			DoActions([
				SetMemory(fpsoffset,SetTo,FPS),
				SetMemory(apmoffset,SetTo,APM),
				SetMemory(peroffset,SetTo,128+APMP),
				SetMemoryX(cycleoffset,SetTo,3,3),
				SGameTime.SetNumber(0),
				SRealTime.SetNumber(0),
				SCount.SetNumber(0),
				Check.SetNumber(1),
			])
		EUDEndIf()

		if EUDIf()((RealTime>=DecValue(N1000))):
			FPS << (10000*GameTime)//RealTime
			MAX << FPS//10+1
			Trigger(conditions=[HCheck.Exactly(1)],actions=[HCheck.SetNumber(0),FPS.SetNumber(DecValue(NFFFF))])	
			APM << Count+1
			Trigger(conditions=[APM >= MAX],actions=[APM.SetNumber(MAX)])
			APMP << (Count*1000)//FPS
			if EUDIf()((FPS <= DecValue(N240)-10)):
				MAX << (FPS*100)//DecValue(N240)
				Trigger(conditions=[APMP.AtLeast(MAX)],actions=[APMP.SetNumber(MAX)])
			EUDEndIf()
			Trigger(conditions=[APMP.AtLeast(101)],actions=[APMP.SetNumber(100)])	
			if EUDExecuteOnce()():
				FPS << 0
				APM << 0
				APMP << 0
			EUDEndExecuteOnce()

			if stackon > 0:
				if stackopt > 0:
					if EUDIf()((ITemp.AtLeast(1), STemp > ETemp, SS == 0, APMP >= STemp)):
						SS << 1 
					EUDEndIf()

					if EUDIf()((SS == 1)):
						DoActions([SNum.AddNumber(1),Stack.AddNumber(APMP)]) # Stack Avg
						EAvg << (DecValue(SRatio)*APMP + (10000-DecValue(SRatio))*EAvg)//10000 # Calc EXP Avg
					EUDEndIf()

					if EUDIf()((SS == 1, SNum >= DecValue(NNum), EAvg <= ETemp)):
						SS << 0
						if EUDIf()(((Stack//SNum) >= ITemp)):
							DoActions([SetMemoryX(cycleoffset,SetTo,8,8)]) # Signal
						EUDEndIf()
						DoActions([
							SS.SetNumber(0),
							SNum.SetNumber(0),
							Stack.SetNumber(0),
							EAvg.SetNumber(0),
						])
					EUDEndIf()
				else:
					if EUDIf()((ITemp.AtLeast(1), STemp > ETemp, SS == 0, APM >= STemp)):
						SS << 1 
					EUDEndIf()

					if EUDIf()((SS == 1)):
						DoActions([SNum.AddNumber(1),Stack.AddNumber(APM)]) # Stack Avg
						EAvg << (DecValue(SRatio)*APM + (10000-DecValue(SRatio))*EAvg)//10000 # Calc EXP Avg
					EUDEndIf()

					if EUDIf()((SS == 1, SNum >= DecValue(NNum), EAvg <= ETemp)):
						SS << 0
						if EUDIf()(((Stack//SNum) >= ITemp)):
							DoActions([SetMemoryX(cycleoffset,SetTo,8,8)]) # Signal
						EUDEndIf()
						DoActions([
							SS.SetNumber(0),
							SNum.SetNumber(0),
							Stack.SetNumber(0),
							EAvg.SetNumber(0),
						])
					EUDEndIf()

			DoActions([
				SetMemory(fpsoffset,SetTo,FPS),
				SetMemory(apmoffset,SetTo,APM),
				SetMemory(peroffset,SetTo,128+APMP),
				SetMemoryX(cycleoffset,SetTo,3,3),
				GameTime.SetNumber(0),
				RealTime.SetNumber(0),
				Count.SetNumber(0),
				Check.SetNumber(0),
			])
		EUDEndIf()

		if stackon > 0 and stacktest > 0:
			DoActions([
				SetMemory(stackoff1,SetTo,SS),
				SetMemory(stackoff2,SetTo,Stack//SNum),
				SetMemory(stackoff3,SetTo,SNum),
				SetMemory(stackoff4,SetTo,EAvg),
			])

		GameTime << EncValue(GameTime)
		SGameTime << EncValue(SGameTime)
		RealTime << EncValue(RealTime)
		SRealTime << EncValue(SRealTime)
		Δu << EncValue(Δu)
		Count << EncValue(Count)
		SCount << EncValue(SCount)

		if stackon > 0:
			SS << EncValue(SS)
			Stack << EncValue(Stack)
			SNum << EncValue(SNum)
			EAvg << EncValue(EAvg)
			DoActions([ITemp.SetNumber(0),STemp.SetNumber(0),ETemp.SetNumber(0)])
	EUDEndIf()

def afterTriggerExec():
	ELoc, Loop, WTemp, W64 = EUDCreateVariables(4)

	Size << f_maskread_epd(DecValue(NE654AA0),0xFFFFFFFF)
	if EUDIf()((ElapsedTime(AtLeast,2))):
		ELoc << EPD(DecValue(N654880)+Size)
		DoActions([SetMemory(Void,SetTo,Size),Loop.SetNumber(0)])
		if EUDIf()((Size > 0)):
			Trigger(conditions=[MemoryX(Void,Exactly,0,3)],actions=[SetDeathsX(ELoc,SetTo,0,0,0xFFFFFFFF)]) # 4
			Trigger(conditions=[MemoryX(Void,Exactly,1,3)],actions=[SetDeathsX(ELoc,SetTo,0,0,0xFFFFFF00)]) # 3
			Trigger(conditions=[MemoryX(Void,Exactly,2,3)],actions=[SetDeathsX(ELoc,SetTo,0,0,0xFFFF0000)]) # 2
			Trigger(conditions=[MemoryX(Void,Exactly,3,3)],actions=[SetDeathsX(ELoc,SetTo,0,0,0xFF000000)]) # 1
			DoActions(ELoc.AddNumber(1),WTemp.SetNumber(DecValue(NE654A70)),W64.SetNumber(DecValue(N64)))
			if EUDWhile()((ELoc < WTemp, Loop < W64)):
				DoActions([
					SetDeaths(ELoc,SetTo,0,0),
					Loop.AddNumber(1),
					ELoc.AddNumber(1),
				])
			EUDEndWhile()
		EUDEndIf()
		DoActions(SetMemory(Void,SetTo,0))
	EUDEndIf()

	if qcmax > 0:
		NewSize = 26+15*qcmax+7 # MSQC PID Size
		if EUDIf()((ElapsedTime(AtLeast,1))):
			# Insert Dummy PID
			DSize, DLoc, P5N, P2N, P5R = EUDCreateVariables(5)
			DSize << NewSize - Size
			if EUDIf()((DSize.AtMost(DecValue(N7FFFFFFF)))):
				P5N << DSize//5
				P5R << DSize%5
				if EUDIf()((EUDOr(P5R == 1, P5R == 3))):
					P2N << (P5R+5)//2
					DoActions(P5N.SubtractNumber(1))
				if EUDElse()():
					P2N << (DSize%5)//2
				EUDEndIf()
				DLoc << DecValue(N654880) + Size

				DoActions([Loop.SetNumber(0)])
				if EUDWhile()((P5N > 0,Loop<P5N)):
					f_bwrite(DLoc,0x12)
					f_dwwrite(DLoc+1,0x00000000)
					DoActions([Loop.AddNumber(1),DLoc.AddNumber(5)])
				EUDEndWhile()

				DoActions([Loop.SetNumber(0)])
				if EUDWhile()((P2N > 0,Loop<P2N)):
					f_wwrite(DLoc,0x060F)
					DoActions([Loop.AddNumber(1),DLoc.AddNumber(2)])
				EUDEndWhile()
				
				Size << NewSize
				DoActions([SetDeaths(DecValue(NE654AA0),SetTo,NewSize,0)])
			EUDEndIf()
		EUDEndIf()

	if debug > 0:
		if EUDIf()((CC == 1)):
			CC << 0
			DoActions(SetDeathsX(Chkepd+0x9C//4,SetTo,f_maskread_epd(EPD(0x654AA0),0xFFFFFFFF),0,0x00FFFFFF))
		EUDEndIf()

		if EUDIf()((DeathsX(Chkepd+0x9C//4,Exactly,0x01000000,0,0xFF000000))):

			PrevCp, Type1, Type2, Type3, Type4, Type5, Line1, Line2, Line3, Line4, Line5, Num2, Check2, Line, Num, Off, Time, Temp, Temp2, CLine, CType, BaseOffset2 = EUDCreateVariables(22)
			PrevCp << f_getcurpl()
			PID = EUDVariable()
			PID << f_maskread_epd(EPD(0x512684), 0xF)
			DoActions(SetCurrentPlayer(PID))

			Line << f_maskread_epd(EPD(0x640B58), 0xF)
			Line1 << Line
			Check2 << 0
			Trigger(conditions=[MemoryX(0x640B58,Exactly,0,1),Check2 == 0],actions=[Type1.SetNumber(0),Check2.SetNumber(1),DisplayText("\x0E\x0D\x0D00000000 \x0D\x0D\x0D00000000 \x1C\x0D\x0D00000000 \x0D\x0D\x0D00000000 \x1F\x0D\x0D00000000 \x0D\x0D\x0D00000000 \x02\x0D\x0D00000000 \x0D\x0D\x0D00000000",4)])
			Trigger(conditions=[MemoryX(0x640B58,Exactly,1,1),Check2 == 0],actions=[Type1.SetNumber(1),Check2.SetNumber(1),DisplayText("\x0D\x0D\x0E\x0D\x0D00000000 \x0D\x0D\x0D00000000 \x1C\x0D\x0D00000000 \x0D\x0D\x0D00000000 \x1F\x0D\x0D00000000 \x0D\x0D\x0D00000000 \x02\x0D\x0D00000000 \x0D\x0D\x0D00000000",4)])
			Line2 << f_maskread_epd(EPD(0x640B58), 0xF)
			Check2 << 0
			Trigger(conditions=[MemoryX(0x640B58,Exactly,0,1),Check2 == 0],actions=[Type2.SetNumber(0),Check2.SetNumber(1),DisplayText("\x18\x0D\x0D00000000 \x0D\x0D\x0D00000000 \x0F\x0D\x0D00000000 \x0D\x0D\x0D00000000 \x07\x0D\x0D00000000 \x0D\x0D\x0D00000000 \x1D\x0D\x0D00000000 \x0D\x0D\x0D00000000",4)])
			Trigger(conditions=[MemoryX(0x640B58,Exactly,1,1),Check2 == 0],actions=[Type2.SetNumber(1),Check2.SetNumber(1),DisplayText("\x0D\x0D\x18\x0D\x0D00000000 \x0D\x0D\x0D00000000 \x0F\x0D\x0D00000000 \x0D\x0D\x0D00000000 \x07\x0D\x0D00000000 \x0D\x0D\x0D00000000 \x1D\x0D\x0D00000000 \x0D\x0D\x0D00000000",4)])
			Line3 << f_maskread_epd(EPD(0x640B58), 0xF)
			Check2 << 0
			Trigger(conditions=[MemoryX(0x640B58,Exactly,0,1),Check2 == 0],actions=[Type3.SetNumber(0),Check2.SetNumber(1),DisplayText("\x03\x0D\x0D00000000 \x17\x0D\x0D00000000 \x19\x0D\x0D00000000 \x04\x0D\x0D00000000 \x15\x0D\x0D00000000 \x11\x0D\x0D00000000 \x1B\x0D\x0D00000000 \x04\x0D\x0D00000000",4)])
			Trigger(conditions=[MemoryX(0x640B58,Exactly,1,1),Check2 == 0],actions=[Type3.SetNumber(1),Check2.SetNumber(1),DisplayText("\x0D\x0D\x03\x0D\x0D00000000 \x17\x0D\x0D00000000 \x19\x0D\x0D00000000 \x04\x0D\x0D00000000 \x15\x0D\x0D00000000 \x11\x0D\x0D00000000 \x1B\x0D\x0D00000000 \x04\x0D\x0D00000000",4)])
			Line4 << f_maskread_epd(EPD(0x640B58), 0xF)
			Check2 << 0
			Trigger(conditions=[MemoryX(0x640B58,Exactly,0,1),Check2 == 0],actions=[Type4.SetNumber(0),Check2.SetNumber(1),DisplayText("\x06\x0D\x0D00000000 \x08\x0D\x0D00000000 \x1B\x0D\x0D00000000 \x04\x0D\x0D00000000 \x10\x0D\x0D00000000 \x1E\x0D\x0D00000000 \x02\x0D\x0D00000000 \x05\x0D\x0D00000000",4)])
			Trigger(conditions=[MemoryX(0x640B58,Exactly,1,1),Check2 == 0],actions=[Type4.SetNumber(1),Check2.SetNumber(1),DisplayText("\x0D\x0D\x06\x0D\x0D00000000 \x08\x0D\x0D00000000 \x1B\x0D\x0D00000000 \x04\x0D\x0D00000000 \x10\x0D\x0D00000000 \x1E\x0D\x0D00000000 \x02\x0D\x0D00000000 \x05\x0D\x0D00000000",4)])
			Line5 << f_maskread_epd(EPD(0x640B58), 0xF)
			Check2 << 0
			Trigger(conditions=[MemoryX(0x640B58,Exactly,0,1),Check2 == 0],actions=[Type5.SetNumber(0),Check2.SetNumber(1),DisplayText("\x0E\x0D\x0D00000000 \x1C\x0D\x0D00000000 \x1F\x0D\x0D00000000 \x0F\x0D\x0D00000000 \x1D\x0D\x0D00000000 \x04\x0D\x0D00000000 \x1B\x0D\x0D00000000 \x05\x0D\x0D00000000",4)])
			Trigger(conditions=[MemoryX(0x640B58,Exactly,1,1),Check2 == 0],actions=[Type5.SetNumber(1),Check2.SetNumber(1),DisplayText("\x0D\x0D\x0E\x0D\x0D00000000 \x1C\x0D\x0D00000000 \x1F\x0D\x0D00000000 \x0F\x0D\x0D00000000 \x1D\x0D\x0D00000000 \x04\x0D\x0D00000000 \x1B\x0D\x0D00000000 \x05\x0D\x0D00000000",4)])

			DoActions([SetMemory(0x640B58,SetTo,Line)])
			DoActions(SetCurrentPlayer(PrevCp))
			 
			BaseOffset2 << Chkptr
			Time << 0
			if EUDWhile()((Time < 5)): 
				Num << 0
				Off << 0
				Trigger(conditions=[Time == 0],actions=[Num2.SetNumber(0),CType.SetNumber(Type1),CLine.SetNumber(Line1)])
				Trigger(conditions=[Time == 1],actions=[Num2.SetNumber(32),CType.SetNumber(Type2),CLine.SetNumber(Line2)])
				Trigger(conditions=[Time == 2],actions=[Num2.SetNumber(64),CType.SetNumber(Type3),CLine.SetNumber(Line3)])
				Trigger(conditions=[Time == 3],actions=[Num2.SetNumber(96),CType.SetNumber(Type4),CLine.SetNumber(Line4)])
				Trigger(conditions=[Time == 4],actions=[Num2.SetNumber(128),CType.SetNumber(Type5),CLine.SetNumber(Line5)])
				if EUDWhile()((Num < 32)): 
					
					if EUDIf()((MemoryX(BaseOffset2 + Num2,AtLeast,0xA,0xF))): 
						Temp << f_maskread_epd(EPD(BaseOffset2 + Num2), 0xF) - 0x9
						Temp2 << 0x40 + Temp
					if EUDElse()():
						Temp << f_maskread_epd(EPD(BaseOffset2 + Num2), 0xF)
						Temp2 << 0x30 + Temp
					EUDEndIf()
					Trigger(conditions=[CType == 0],actions=[SetMemoryX(0x640B68 + CLine*218 + Off, SetTo, Temp2*65536,0xFF0000)])
					Trigger(conditions=[CType == 1],actions=[SetMemoryX(0x640B6A + CLine*218 + Off, SetTo, Temp2*65536,0xFF0000)])

					if EUDIf()((MemoryX(BaseOffset2 + Num2,AtLeast,0xA0,0xF0))): 
						Temp << f_maskread_epd(EPD(BaseOffset2 + Num2), 0xF0) - 0x90
						Temp2 << 0x40 + Temp//0x10
					if EUDElse()():
						Temp << f_maskread_epd(EPD(BaseOffset2 + Num2), 0xF0)
						Temp2 << 0x30 + Temp//0x10
					EUDEndIf()
					Trigger(conditions=[CType == 0],actions=[SetMemoryX(0x640B68 + CLine*218 + Off, SetTo, Temp2*256,0xFF00)])
					Trigger(conditions=[CType == 1],actions=[SetMemoryX(0x640B6A + CLine*218 + Off, SetTo, Temp2*256,0xFF00)])

					if EUDIf()((MemoryX(BaseOffset2 + Num2,AtLeast,0xA00,0xF00))): 
						Temp << f_maskread_epd(EPD(BaseOffset2 + Num2), 0xF00) - 0x900
						Temp2 << 0x40 + Temp//0x100
					if EUDElse()():
						Temp << f_maskread_epd(EPD(BaseOffset2 + Num2), 0xF00)
						Temp2 << 0x30 + Temp//0x100
					EUDEndIf()
					Trigger(conditions=[CType == 0],actions=[SetMemoryX(0x640B68 + CLine*218 + Off, SetTo, Temp2*1,0xFF)])
					Trigger(conditions=[CType == 1],actions=[SetMemoryX(0x640B6A + CLine*218 + Off, SetTo, Temp2*1,0xFF)])

					if EUDIf()((MemoryX(BaseOffset2 + Num2,AtLeast,0xA000,0xF000))): 
						Temp << f_maskread_epd(EPD(BaseOffset2 + Num2), 0xF000) - 0x9000
						Temp2 << 0x40 + Temp//0x1000
					if EUDElse()():
						Temp << f_maskread_epd(EPD(BaseOffset2 + Num2), 0xF000)
						Temp2 << 0x30 + Temp//0x1000
					EUDEndIf()
					Trigger(conditions=[CType == 0],actions=[SetMemoryX(0x640B64 + CLine*218 + Off, SetTo, Temp2*16777216,0xFF000000)])
					Trigger(conditions=[CType == 1],actions=[SetMemoryX(0x640B66 + CLine*218 + Off, SetTo, Temp2*16777216,0xFF000000)])

					if EUDIf()((MemoryX(BaseOffset2 + Num2,AtLeast,0xA0000,0xF0000))): 
						Temp << f_maskread_epd(EPD(BaseOffset2 + Num2), 0xF0000) - 0x90000
						Temp2 << 0x40 + Temp//0x10000
					if EUDElse()():
						Temp << f_maskread_epd(EPD(BaseOffset2 + Num2), 0xF0000)
						Temp2 << 0x30 + Temp//0x10000
					EUDEndIf()
					Trigger(conditions=[CType == 0],actions=[SetMemoryX(0x640B64 + CLine*218 + Off, SetTo, Temp2*65536,0xFF0000)])
					Trigger(conditions=[CType == 1],actions=[SetMemoryX(0x640B66 + CLine*218 + Off, SetTo, Temp2*65536,0xFF0000)])

					if EUDIf()((MemoryX(BaseOffset2 + Num2,AtLeast,0xA00000,0xF00000))): 
						Temp << f_maskread_epd(EPD(BaseOffset2 + Num2), 0xF00000) - 0x900000
						Temp2 << 0x40 + Temp//0x100000
					if EUDElse()():
						Temp << f_maskread_epd(EPD(BaseOffset2 + Num2), 0xF00000)
						Temp2 << 0x30 + Temp//0x100000
					EUDEndIf()
					Trigger(conditions=[CType == 0],actions=[SetMemoryX(0x640B64 + CLine*218 + Off, SetTo, Temp2*256,0xFF00)])
					Trigger(conditions=[CType == 1],actions=[SetMemoryX(0x640B66 + CLine*218 + Off, SetTo, Temp2*256,0xFF00)])

					if EUDIf()((MemoryX(BaseOffset2 + Num2,AtLeast,0xA000000,0xF000000))): 
						Temp << f_maskread_epd(EPD(BaseOffset2 + Num2), 0xF000000) - 0x9000000
						Temp2 << 0x40 + Temp//0x1000000
					if EUDElse()():
						Temp << f_maskread_epd(EPD(BaseOffset2 + Num2), 0xF000000)
						Temp2 << 0x30 + Temp//0x1000000
					EUDEndIf()
					Trigger(conditions=[CType == 0],actions=[SetMemoryX(0x640B64 + CLine*218 + Off, SetTo, Temp2*1,0xFF)])
					Trigger(conditions=[CType == 1],actions=[SetMemoryX(0x640B66 + CLine*218 + Off, SetTo, Temp2*1,0xFF)])

					if EUDIf()((MemoryX(BaseOffset2 + Num2,AtLeast,0xA0000000,0xF0000000))): 
						Temp << f_maskread_epd(EPD(BaseOffset2 + Num2), 0xF0000000) - 0x90000000
						Temp2 << 0x40 + Temp//0x10000000
					if EUDElse()():
						Temp << f_maskread_epd(EPD(BaseOffset2 + Num2), 0xF0000000)
						Temp2 << 0x30 + Temp//0x10000000
					EUDEndIf()
					Trigger(conditions=[CType == 0],actions=[SetMemoryX(0x640B60 + CLine*218 + Off, SetTo, Temp2*16777216,0xFF000000)])
					Trigger(conditions=[CType == 1],actions=[SetMemoryX(0x640B62 + CLine*218 + Off, SetTo, Temp2*16777216,0xFF000000)])

					Num << Num + 4
					Off << Off + 12
					Num2 << Num2 + 4
				EUDEndWhile()
				Time << Time + 1
			EUDEndWhile()
		EUDEndIf()

		Trigger(conditions=[MemoryX(0x596A90, Exactly, 16777216, 0xFF000000)],actions=[SetDeathsX(Chkepd+0x9C//4,SetTo,0,0,0xFF000000)])
