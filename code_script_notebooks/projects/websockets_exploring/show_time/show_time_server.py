import asyncio
import datetime
import random
import websockets


async def stime(websocket):
    while True:
        message = datetime.datetime.now().isoformat() + "Z"
        await websocket.send(message)
        await asyncio.sleep(random.random() * 2 + 1)


async def main():
    async with websockets.serve(stime, "localhost", 7956):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())