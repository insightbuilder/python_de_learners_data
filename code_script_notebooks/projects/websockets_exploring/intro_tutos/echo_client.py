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
# methods and attrs in websy object
# 'acknowledge_pings', 'close', 'close_deadline', 'close_socket',
# 'close_timeout', 'debug', 'handshake', 'id', 'local_address',
# 'logger', 'ping', 'pings', 'pong', 'process_event', 'protocol',
# 'protocol_mutex', 'recv', 'recv_bufsize', 'recv_events', 'recv_events_exc',
# 'recv_events_thread', 'recv_messages', 'recv_streaming', 'remote_address',
# 'request', 'response', 'response_rcvd', 'send', 'send_context', 'send_data',
# 'send_in_progress', 'set_recv_events_exc', 'socket', 'subprotocol'
        while True:
            serve_input = input("What is the input? ")
            websy.send(serve_input)
            message = websy.recv()
            print(message)


# hello()
while_hello()