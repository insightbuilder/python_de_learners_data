from websockets.sync.client import connect


with connect("ws://localhost:8002/") as websb:
    print(dir(websb))
    print('Established connect...')
    while True:
        data = input("What you wanna send? ")
        req = websb.send(data)
        print(req)  # as such the send method will return None
        ret_resp = websb.recv()
        print(ret_resp)
