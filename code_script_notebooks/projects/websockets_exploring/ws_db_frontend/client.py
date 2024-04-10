import asyncio
from websockets import connect
import json

async def say_hi():
    async with connect("ws://localhost:7568/") as websy:
        while True:
            data_in = input("Provide data: ")
            data_dict = {"input": data_in}
            data_str = json.dumps(data_dict)
            await websy.send(data_str)
            ret_msg = await websy.recv()
            print(ret_msg)


if __name__ == '__main__':
    asyncio.run(say_hi())