import asyncio
import websockets
import pathlib
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_verify_locations(localhost_pem)


async def hello():
    # url = "ws://localhost:8888/"
    url = "wss://localhost:8765/"
    async with websockets.connect(url, ssl=ssl_context) as websy:
        while True:
            name = input("Getting name: ")

            await websy.send(f"Your name is {name}")

            recved_greet = await websy.recv()
            print(f"<<< {recved_greet}")
            if name == 'enough':
                break


if __name__ == "__main__":
    asyncio.run(hello())