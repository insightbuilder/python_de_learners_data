import asyncio
from websockets import serve
import json
from models import Mynotes


async def handler(websocket):
    async for msg in websocket:
        get_json = json.loads(msg)
        if 'payload' in get_json:
            print(get_json['payload'])
            # payload is containing dict of 
            # heading & content
            if get_json['payload'] == 'list':
                notes = []
                for x in Mynotes.select():
                    notes.append({
                        "heading": x.heading,
                        "content": x.content
                    })
                get_json['db_data'] = notes
                get_json.pop('payload')
                json_str = json.dumps(get_json)
            else:
                m1 = Mynotes(**get_json['payload'])
                m1.save()
                get_json['reply'] = 'Saved'
                get_json.pop('payload')
                json_str = json.dumps(get_json)
            
            await websocket.send(json_str)
        print('No Payload...')


async def main():
    async with serve(handler, 'localhost', 6655):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
