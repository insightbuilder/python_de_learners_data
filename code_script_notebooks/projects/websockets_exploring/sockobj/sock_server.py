from websockets import serve
import asyncio
import json
import random


async def handler(websocket):
    print(websocket.path)
    print(websocket.request_headers)
    ind = 0
    try:
        async for msg in websocket:
            print(msg)
            while True:
                send_msg = f"Acknowledged {ind}"
                await websocket.send(send_msg)
                await asyncio.sleep(random.random() * 5)
                ind += 1
                if ind % 2 == 0:
                    await websocket.send("Wanna Continue???")
                    int_data = await websocket.recv()
                    if int_data == 'close':
                        await websocket.send('Closing Tap...')
                        break
                    await websocket.send("Okay Loop continued...")
    except Exception as e:
        await websocket.send(f"Connnection Closed...{e}")


async def main():
    async with serve(handler, 'localhost', 7568):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
