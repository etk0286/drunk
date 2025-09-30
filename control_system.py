import asyncio
import websockets
import socket

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print("server IP:", ip_address)

clients = {}  #  {client_id: websocket}

async def handler(websocket):
    try:
        #
        client_id = await websocket.recv()
        clients[client_id] = websocket
        print(f"[Server] {client_id} Connected")

        # keep receive
        async for message in websocket:
            print(f"[{client_id}] receive: {message}")

    except Exception as e:
        print(f"[Server] {client_id} disconnect: {e}")
    finally:
        if client_id in clients:
            del clients[client_id]

# send messenge to your clien
async def send_to(client_id, message):
    if client_id in clients:
        await clients[client_id].send(message)
        print(f"[Server] SEND {client_id}: {message}")
    else:
        print(f"[Server] Can't find {client_id}")

# read terminal
async def terminal_input():
    while True:
        cmd = await asyncio.to_thread(input, "terminal > ")
        if cmd.startswith("send "):
            try:
                _, client_id, msg = cmd.split(" ", 2)
                await send_to(client_id, msg)
            except:
                print("error: send ESP32_A Hello")

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket Server open ws://0.0.0.0:8765")
        await asyncio.gather(terminal_input(), asyncio.Future())  # server never end

asyncio.run(main())
