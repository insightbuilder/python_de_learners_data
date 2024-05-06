import asyncio
from websockets import connect
import json


async def take_notes():
    async with connect('ws://localhost:6655/') as webs:
        while True:
            heading = input("Notes heading or List notes: ")
            if heading == 'list':
                print('Get Notes list')
                json_str = json.dumps({"payload": 'list'})
                await webs.send(json_str)
                data = await webs.recv()
                print(data)
            else:
                content = input("Notes content: ")
                notes = {
                    "heading": heading,
                    "content": content
                }
                json_str = json.dumps({"payload": notes})
                await webs.send(json_str)
                ack = await webs.recv()
                print(ack)


if __name__ == '__main__':
    asyncio.run(take_notes())
