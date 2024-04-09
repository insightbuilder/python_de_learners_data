import asyncio
import websockets
import json
from connect4 import PLAYER1, PLAYER2, Connect4
import itertools

async def game_handler(websocket):
    game = Connect4()
    
    turns = itertools.cycle([PLAYER1, PLAYER2])
    player = next(turns)

    for player, column, row in [
        (PLAYER1, 3, 0),
        (PLAYER2, 3, 1),
        (PLAYER1, 4, 0),
        (PLAYER2, 4, 1),
        (PLAYER1, 2, 0),
        (PLAYER2, 1, 0),
        (PLAYER1, 5, 0),
    ]:
        event = {
            "type": "play",
            "player": player,
            "column": column,
            "row": row
        }
        await websocket.send(json.dumps(event))
        await asyncio.sleep(0.5)

    event = {
        "type": "win",
        "player": PLAYER1
    }
    await websocket.send(json.dumps(event))

# async def handler(websocket):  # allows the close connection gracefully
    # while True:
        # try:
            # message = await websocket.recv()
        # except websockets.ConnectionClosedOK:
            # break
        # async for message in websocket:
            # print(message)

# handler is a coroutine that manages a connection. When a client connects,
# websockets calls handler with the connection in argument. When handler
# terminates, websockets closes the connection.

# The second argument defines the network interfaces where the server can be
# reached. Here, the server listens on all interfaces, so that other devices
# on the same local network can connect.

# The third argument is the port on which the server listens.


async def main():
    async with websockets.serve(game_handler, "", 8001):  # server needs to have the handler
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
