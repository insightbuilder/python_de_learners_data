# server.py

import asyncio
import websockets
import lxml.objectify


async def handle_connection(websocket, path):
    async for message in websocket:
        try:
            xml = lxml.objectify.fromstring(message)
        except SyntaxError:
            print("Malformed XML message:", repr(message))
        else:
            if xml.tag == "KeyboardEvent":
                if xml.Type == "keyup":
                    print("Key:", xml.Key.Unicode)
            elif xml.tag == "MouseEvent":
                screen = xml.Cursor.Screen
                print("Mouse:", screen.get("x"), screen.get("y"))
            else:
                print("Unrecognized event type")


if __name__ == "__main__":
    future = websockets.serve(handle_connection, "localhost", 8000)
    asyncio.get_event_loop().run_until_complete(future)
    asyncio.get_event_loop().run_forever()