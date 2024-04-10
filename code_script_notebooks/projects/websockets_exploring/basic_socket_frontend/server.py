import asyncio
from websockets import (
    serve,
    broadcast
)
import json
from models import Payload
from peewee import SqliteDatabase

db = SqliteDatabase("warmup.db")
db.connect()
SESS = set()
USERS = 0


async def handler(websocket):
    global SESS, USERS
    try:
        SESS.add(websocket)
        USERS += 1
        broadcast(SESS, json.dumps({"counts": USERS}))

        async for message in websocket:
            msg_packet = json.loads(message)
            print(msg_packet)
            process_msg = msg_packet['payload']
            process_msg = f"Recieved Message: {process_msg}"
            msg_packet['packet'] = process_msg
            save_pl = Payload.create(**msg_packet)
            save_pl.save()
            reply_msg = json.dumps(msg_packet)
            await websocket.send(reply_msg)
        
        print("after await...")
    finally:
        SESS.remove(websocket)
        USERS -= 1
        broadcast(SESS, json.dumps({"counts": USERS}))


async def main():
    async with serve(handler, 'localhost', 7555):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
