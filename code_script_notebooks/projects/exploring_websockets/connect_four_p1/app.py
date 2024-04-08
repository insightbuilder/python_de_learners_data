import asyncio
import websockets


async def handler(websocket):  # allows the close connection gracefully
    while True:
#         try:
            # message = await websocket.recv()
        # except websockets.ConnectionClosedOK:
            # break
        async for message in websocket:
            print(message)

# handler is a coroutine that manages a connection. When a client connects,
# websockets calls handler with the connection in argument. When handler
# terminates, websockets closes the connection.

# The second argument defines the network interfaces where the server can be
# reached. Here, the server listens on all interfaces, so that other devices
# on the same local network can connect.

# The third argument is the port on which the server listens.

async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())