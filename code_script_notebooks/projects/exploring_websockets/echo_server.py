import asyncio
from websockets.server import serve


async def echo(websocket):  # async function, with websocket object
    # print(type(websocket))  # <class 'websockets.legacy.server.WebSocketServerProtocol'>
    # similar to the request recieved from webserver.. Here its a socket
    async for message in websocket:
        print(message)
        length = f"Message {message} is of {len(message)} char long"
        await websocket.send(length)


async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()

asyncio.run(main())
