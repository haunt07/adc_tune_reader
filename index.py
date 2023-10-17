#!/Users/fachri/programming/test/testNotif/venv/bin/python
import asyncio
from queue import Queue
from pathlib import Path

#Const Variable
global triggerADC
triggerADC=1  #adc arduino > 50 #adc raspberry > 1 Mas Fandi tunning tegangan

que=Queue()
sReading=False
global sProcess
sProcess=0
# path = Path(__file__).resolve().parent.joinpath("CHOL_UA_Strip dicabut saat counting down.txt")
path = Path(__file__).resolve().parent.joinpath("log_strip_masuk_berhasil,hasil_berhasil.txt")
# path = Path(__file__).resolve().parent.joinpath("log_strip_masuk_berhasil,hasil_gagal_low.txt")
# path = Path(__file__).resolve().parent.joinpath("log_strip_masuk_berhasil.txt")
# path = Path(__file__).resolve().parent.joinpath("log_strip_masuk_eror.txt")

def processResult(value):
    que.put(value)

# async def readSensor():
#     with open(path) as fs:
#         for val in fs:
#             processResult(val.split()[2])
#             await asyncio.sleep(0.0001)

async def readSensor():
    while True:
        #TODO Program mas Fandi disini
        
        # processResult(variableHasilDisini) <-- Masukan nilainya disini 
        await asyncio.sleep(0.0001)

def processSensor(mRSound:str):
    global sProcess
    if mRSound=="s":
        if sProcess==0:
            print("Strip Masuk")
        elif sProcess==1:
            print("Blood Masuk")
        elif sProcess==3:
            print("Strip Dicabut")
        else:
            print("Device Signal Error")
            sProcess=0
        sProcess+=1
    elif mRSound=="ss":
        if sProcess==2:
            print("Keluar Hasil")
        else:
            print("Device Signal Error")
            sProcess=0
        sProcess+=1
    elif mRSound=="l":
        if sProcess==1:
            print("Strip dicabut")
        else:
            print("Device Shutdown")
        sProcess=0
    elif mRSound=="sssss":
        if sProcess==0:
            print("Strip Error")
        elif sProcess==1:
            print("Pengambilan Darah Error")
        elif sProcess==2:
            print("Pembacaan Darah Error")
        elif sProcess==3:
            print("Hasil Pembacaan Darah Error")
        else:
            print("Device Error")
        sProcess=0

async def main():
    global triggerADC
    asyncio.create_task(readSensor())
    await asyncio.sleep(0.01)
    sReading=False
    mHCount=0
    mLCount=0
    mRSound=""
    while not que.empty():
        dt = que.get()
        logicDt = True if float(dt) > triggerADC else False

        if sReading == False and logicDt:
            sReading = True
            mHCount = 0
            mLCount = 0
        elif sReading and logicDt:
            mHCount += 1
        elif sReading and logicDt==False:
            mLCount+=1
            if mLCount >= 2:
                mRSound+="l" if mHCount >5 else "s"
                sReading = False
        elif mRSound !="":
            mLCount+=1
            if mLCount > 10:
                processSensor(mRSound)
                mRSound=""
        await asyncio.sleep(0.001)

asyncio.run(main())