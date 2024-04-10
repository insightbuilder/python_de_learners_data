import asyncio
import json
from websockets import serve, broadcast
from peewee import SqliteDatabase
from models import Payload

db = SqliteDatabase('trial.db')
db.connect()


async def handler(websocket):
    async for msg in websocket:
        data = json.loads(msg)
        print(data)
        if 'input' in data:
            data['output'] = f"Updated message: {data['input']}"
            out_data = json.dumps(data)
            data_db = Payload.create(input_text=data['input'],
                                    output_text=data['output'])
            data_db.save()
            await websocket.send(out_data)
        elif 'database' in data:
            db_data = Payload.select()
            db_payload = []
            for d in db_data:
                db_payload.append({
                    "input_text": d.input_text,
                    "output_text": d.output_text
                })
            db_data_str = json.dumps({"db_data": db_payload})
            await websocket.send(db_data_str)

async def main():
    async with serve(handler, 'localhost', 7568):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
