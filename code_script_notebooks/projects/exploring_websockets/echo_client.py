import asyncio
from websockets.sync.client import connect

def hello():
    with connect("ws://localhost:8765") as websy:
        for nid in range(3):
            websy.send(f"Hello {nid}")
            # only first send will get the reciept back
        message = websy.recv()
        print(f"Recieved: {message}")


def while_hello():
    with connect("ws://localhost:8765") as websy:
        while True:
            serve_input = input("What is the input? ")
            websy.send(serve_input)
            message = websy.recv()
            print(message)


# hello()
while_hello()