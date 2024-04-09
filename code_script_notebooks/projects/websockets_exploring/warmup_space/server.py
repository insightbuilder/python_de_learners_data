from websockets import serve
import asyncio


async def handler(websocket):
    async for message in websocket:
        print(message) 
        await websocket.send(f"returning from server: {message}")


async def main():
    async with serve(handler, "", 8002):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
