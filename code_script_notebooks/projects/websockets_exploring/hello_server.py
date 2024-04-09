import asyncio
import websockets
import ssl
import pathlib


async def hello(websocket):
    async for message in websocket:
        print(f"Recieving message: {message}")
        make_msg = f"updated message: {message}"
        await websocket.send(make_msg)

print(ssl.PROTOCOL_TLS_SERVER)
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_cert_chain(localhost_pem)

async def main():
    async with websockets.serve(hello, "localhost", 8765, ssl=ssl_context):
        await asyncio.Future()

if __name__ == '__main__':
    asyncio.run(main())