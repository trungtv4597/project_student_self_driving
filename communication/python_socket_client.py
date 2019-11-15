import websockets
import asyncio # The Python package that provides a foundation and API for running and managing coroutines
               # Coroutines (specialized generator functions)


async def hello():
    uri = 'ws://192.168.1.2:4567/' # In this case, the IP address of the ESP8266 and its port
    async with websockets.connect(uri) as websocket:
        name = input('whats your name?')

        await websocket.send(name)
        print(f'> {name}')

        greeting = await websocket.recv()
        print(f'< {greeting}')

asyncio.get_event_loop().run_until_complete(hello())