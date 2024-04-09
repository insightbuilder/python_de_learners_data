import asyncio
import json
import logging
import websockets

logging.basicConfig(level=logging.INFO,
                    format="%(message)s|%(asctime)s")

USERS = set()

VALUE = 0


def users_event():
    return json.dumps({"type": "users",
                       "count": len(USERS)})


def value_event():
    return json.dumps({"type": "value", 
                       "value": VALUE})


async def counter(websocket):
    global USERS, VALUE

    try:
        USERS.add(websocket)
        websockets.broadcast(USERS, users_event())

        await websocket.send(value_event())
        async for message in websocket:
            event = json.loads(message)
            if event["action"] == "minus":
                logging.info(event)
                VALUE -= 1
                websockets.broadcast(USERS, value_event())
            elif event["action"] == "plus":
                VALUE += 1
                websockets.broadcast(USERS, value_event())
            else:
                logging.error(f"Unsupported: {event}")
        
    finally:
        USERS.remove(websocket)
        websockets.broadcast(USERS, users_event())


async def main():
    async with websockets.serve(counter, "localhost", 7777):
        await asyncio.Future()
    

if __name__ == "__main__":
    asyncio.run(main())