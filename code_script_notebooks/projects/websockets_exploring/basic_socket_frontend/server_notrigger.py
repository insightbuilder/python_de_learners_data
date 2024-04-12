import asyncio
from websockets import (
    serve,
)
import json
import random


async def handler(websocket):
    msg_packet = {}
    ind = 0 
    while True:
        process_msg = f"Sending Message: {ind}"
        msg_packet['packet'] = process_msg
        reply_msg = json.dumps(msg_packet)
        print(reply_msg)
        ind += 1
        await websocket.send(reply_msg) 
        await asyncio.sleep(random.random() * 2 + 1)

async def main():
    async with serve(handler, 'localhost', 7555):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
