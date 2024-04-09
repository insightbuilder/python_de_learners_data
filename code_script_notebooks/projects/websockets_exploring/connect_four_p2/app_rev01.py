import asyncio
import websockets
import json
from connect4 import PLAYER1, PLAYER2, Connect4
import itertools
import secrets  # this is new module

JOIN = {}  # this stores the session secrets and connections
WATCH = {}  # stores the watchers secrets


async def error(websocket, message):
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))


async def replay(websocket, game):
    """Send all moves till now..."""
    for player, column, row in game.moves.copy():
        event = {
            "type": "play",
            "player": player,
            "column": column,
            "row": row
        }
        await websocket.send(json.dumps(event))


async def play(websocket, game, player, connected):
    "Process the Moves from players"
    async for messages in websocket:
        event = json.loads(messages)
        assert event['type'] == 'play'
        column = event['column']

        try:
            row = game.play(player, column)
        except RuntimeError as exc:
            await error(websocket, str(exc))
            continue

    event = {
        "type": "play",
        "player": player,
        "column": column,
        "row": row
    }

    websockets.broadcast(connected, json.dumps(event))

    if game.winner is not None:
        event = {
            "type": "win",
            "player": game.winner
        }

        websockets.broadcast(connected, json.dumps(event))


async def start(websocket):
    game = Connect4()
    connected = {websocket}

    join_key = secrets.token_urlsafe(12)
    JOIN[join_key] = game, connected

    watch_key = secrets.token_urlsafe(12)
    WATCH[watch_key] = game, connected

    try:
        event = {
            "type": "init",
            "join": join_key,
            "watch": watch_key,
        }
        await websocket.send(json.dumps(event))

        print(f"Player 1 is in the game, {id(game)}")

        async for message in websocket:
            print(f"First player sent: {message}")
 
    finally:
        del JOIN[join_key]
        del WATCH[watch_key]


async def join(websocket, join_key):
    try:
        game, connected = JOIN[join_key]
    except KeyError:
        await error(websocket, "Game not found.")
        return

    connected.add(websocket)

    try:
        await replay(websocket, game)
        async for message in websocket:
            print(f"This is from joined player: {message}")
        await play(websocket, game, PLAYER2, connected)

    finally:
        connected.remove(websocket)


async def watch(websocket, watch_key):
    """
    Handle a connection from a spectator: watch an existing game.

    """
    # Find the Connect Four game.
    try:
        game, connected = WATCH[watch_key]
    except KeyError:
        await error(websocket, "Game not found.")
        return

    # Register to receive moves from this game.
    connected.add(websocket)
    try:
        # Send previous moves, in case the game already started.
        await replay(websocket, game)
        # Keep the connection open, but don't receive any messages.
        await websocket.wait_closed()
    finally:
        connected.remove(websocket)


async def game_handler(websocket):
    message = await websocket.recv()
    event = json.loads(message)
    assert event['type'] == 'init'

    if "join" in event:
        await join(websocket, event['join'])
    elif "watch" in event:
        await watch(websocket, event['watch'])
    else:
        await start(websocket)


async def main():
    async with websockets.serve(game_handler, "", 8001):
        # server needs to have the handler
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    asyncio.run(main())
