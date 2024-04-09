import asyncio
import datetime
import random
import websockets


connections = set()


async def register(websocket):
    connections.add(websocket)  # socket objects are stored
    try:
        await websocket.wait_closed()  # chek if there is a client
 
    finally:
        connections.remove(websocket)  # remove the socket if gone


async def show_time():
    while True:
        message = datetime.datetime.now().isoformat() + "Z"
        websockets.broadcast(connections, message)
        await asyncio.sleep(random.random() * 2 + 1)


async def main():
    async with websockets.serve(register, "localhost", 5678):
        await show_time()


if __name__ == "__main__":
    asyncio.run(main())