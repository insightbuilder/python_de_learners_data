import asyncio
import websockets
import json
from connect4 import PLAYER1, PLAYER2, Connect4
import itertools


async def game_handler(websocket):
    game = Connect4()
    
    turns = itertools.cycle([PLAYER1, PLAYER2])
    player = next(turns)

    async for message in websocket:
        event = json.loads(message)
        assert event["type"] == "play"
        column = event["column"]

        try:
            row = game.play(player, column)
        except RuntimeError as ext:
            event = {
                "type": "error",
                "message": str(ext)
            }
            await websocket.send(json.dumps(event))
            continue
    
        event = {
            "type": "play",
            "player": player,
            "column": column,
            "row": row
        }
        await websocket.send(json.dumps(event))

        if game.winner is not None:
            event = {
                "type": "win",
                "player": game.winner
            }
            await websocket.send(json.dumps(event))
 
        player = next(turns)


async def main():
    async with websockets.serve(game_handler, "", 8001):  # server needs to have the handler
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
