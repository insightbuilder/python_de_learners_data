import asyncio
import random
import json
import websockets

async def send_data(websocket, path):
    while True:
        # Generate random temperature and humidity data
        temperature = round(random.uniform(20, 30), 2)
        humidity = round(random.uniform(40, 60), 2)
        
        # Create a JSON message containing temperature and humidity data
        data = {
            'temperature': temperature,
            'humidity': humidity
        }
        message = json.dumps(data)
        
        # Send the JSON message to the client
        await websocket.send(message)
        
        # Wait for 1 second before sending the next data
        await asyncio.sleep(1)

# Start the WebSocket server on localhost, port 8765
start_server = websockets.serve(send_data, "localhost", 8765)

# Run the WebSocket server indefinitely
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
