#!/Users/fachri/programming/test/testNotif/venv/bin/python
import asyncio
from queue import Queue
from pathlib import Path

#Const Variable
global triggerADC
triggerADC=1  #adc raspberry > 100 Mas Fandi tunning tegangan

#Global Variable
que=Queue()
sReading=False
global sProcess
global sRun

async def readSensor():
    while True:
        #TODO Program mas Fandi disini
        
        # processResult(variableHasilDisini) <-- Masukan nilainya disini. nilainya int atau float
        await asyncio.sleep(0.0001)
    
# async def readSensor():
#     path = Path(__file__).resolve().parent.joinpath("resultTestSensorGlucose/GLU_BERHASIL_SEMUA.txt")
#     # path = Path(__file__).resolve().parent.joinpath("resultTestSensorGlucose/GLU_STRIPMASUK_NORMAL.txt")
#     #path = Path(__file__).resolve().parent.joinpath("resultTestSensorGlucose/GLU_STRIPMASUK_ERROR.txt")
#     global sRun
#     with open(path) as fs:
#         iter=0
#         for val in fs:
#             processResult(val.split()[2])
#             await asyncio.sleep(0.0001)
#     sRun=False
    
def processResult(value):
    que.put(value)

def processSensor(mRSound:str):
    if mRSound=="s":
        print("Next Step")
    elif mRSound=="ss":
        print("Strip Error")

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
                    mRSound+="l" if mHCount >10 else "s"
                    sReading = False
            elif mRSound !="":
                mLCount+=1
                if mLCount > 10:
                    processSensor(mRSound)
                    mRSound=""
        await asyncio.sleep(0.001)

asyncio.run(main())