import asyncio
from websockets import connect
import json

async def say_hi():
    async with connect("ws://localhost:7555") as websy:
        while True:
            input_text = input('tell me: ')
            payload_text = json.dumps({"payload": input_text})
            await websy.send(payload_text)
            reply_msg = await websy.recv()
            print(reply_msg)


if __name__ == "__main__":
    asyncio.run(say_hi())