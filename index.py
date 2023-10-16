import asyncio
from queue import Queue
from pathlib import Path

que=Queue()
sState=False
path = Path(__file__).resolve().parent.joinpath("log_strip_masuk_berhasil,hasil_berhasil.txt")
# path = Path(__file__).resolve().parent.joinpath("log_strip_masuk_berhasil,hasil_gagal_low.txt")
# path = Path(__file__).resolve().parent.joinpath("log_strip_masuk_berhasil.txt")
# path = Path(__file__).resolve().parent.joinpath("log_strip_masuk_eror.txt")

async def readSensor():
    with open(path) as fs:
        for val in fs:
            que.put(val.split()[2])
            await asyncio.sleep(0.0001)

#!/Users/fachri/programming/test/testNotif/venv/bin/python
async def main():
    asyncio.create_task(readSensor())
    await asyncio.sleep(0.01)
    sState=False
    mHCount=0
    mLCount=0
    mRSound=""
    while not que.empty():
        dt = que.get()
        logicDt = True if float(dt) > 1 else False
        # print(logicDt)
        if sState == False and logicDt:
            sState = True
            mHCount = 0
            mLCount = 0
        elif sState and logicDt:
            mHCount += 1
        elif sState and logicDt==False:
            mLCount+=1
            if mLCount >= 2:
                mRSound+="l" if mHCount >5 else "s"
                sState = False
        elif mRSound !="":
            mLCount+=1
            if mLCount > 10:
                print(mRSound)
                mRSound=""
        await asyncio.sleep(0.001)

asyncio.run(main())