#!/Users/fachri/programming/test/testNotif/venv/bin/python
import asyncio
from queue import Queue
from pathlib import Path

#Const Variable
global triggerADC
triggerADC=1  #adc arduino > 50 #adc raspberry > 1 Mas Fandi tunning tegangan

#Global Variable
que=Queue()
sReading=False
global sProcess
global sRun
sProcess=0

async def readSensor():
    while True:
        #TODO Program mas Fandi disini
        
        # processResult(variableHasilDisini) <-- Masukan nilainya disini. nilainya int atau float
        await asyncio.sleep(0.0001)
    
# async def readSensor():
#     # path = Path(__file__).resolve().parent.joinpath("resultTestSensorUA/CHOL_UA_Strip dicabut saat counting down.txt")
#     path = Path(__file__).resolve().parent.joinpath("resultTestSensorUA/log_strip_masuk_berhasil,hasil_berhasil.txt")
#     # path = Path(__file__).resolve().parent.joinpath("resultTestSensorUA/log_strip_masuk_berhasil,hasil_gagal_low.txt")
#     # path = Path(__file__).resolve().parent.joinpath("resultTestSensorUA/log_strip_masuk_berhasil.txt")
#     # path = Path(__file__).resolve().parent.joinpath("resultTestSensorUA/log_strip_masuk_eror.txt")
#     global sRun
#     with open(path) as fs:
#         for val in fs:
#             processResult(val.split()[2])
#             await asyncio.sleep(0.0001)
#     sRun=False
    
def processResult(value):
    que.put(value)

def processSensor(mRSound:str):
    global sProcess
    if mRSound=="s":
        if sProcess==0:
            print("Strip Masuk")
            sProcess+=1
        elif sProcess==1:
            print("Blood Masuk")
            sProcess+=1
        elif sProcess==3:
            print("Strip Dicabut")
            sProcess=0
        else:
            print("Device Signal Error")
            sProcess=0
    elif mRSound=="ss":
        if sProcess==2:
            print("Keluar Hasil")
            sProcess+=1
        else:
            print("Device Signal Error")
            sProcess=0
    elif mRSound=="l":
        if sProcess==1:
            print("Strip dicabut")
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
    global sRun
    asyncio.create_task(readSensor())
    await asyncio.sleep(0.01)
    sReading=False
    mHCount=0
    mLCount=0
    mRSound=""
    sRun=True
    while sRun:
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