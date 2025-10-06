import asyncio
import websockets
import socket
import json
from datetime import datetime
date=datetime.now()
now_date=date.strftime("%Y-%m-%d %H-%M-%S")# get current date and time

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)
print("server IP:", ip_address)

clients = {}     #{client_id: websocket}
save_message=[]  #[client_id,123]

async def handler(websocket):
    try:
        #
        client_id = await websocket.recv()
        clients[client_id] = websocket
        print(f"[Server] {client_id} Connected")

        # keep receive
        async for message in websocket:
            with open("item.json", "r", encoding="utf-8") as f:
                item = json.load(f)

            print(f"[{client_id}] receive: {message}")
            new_data=[now_date,client_id,message]

            decode_data=[new_data[2]]

            if new_data[1]=="client1":  ####

                with open("data1.json", "r") as f:
                    loaded_data = json.load(f)
                print("loaded_data1:",loaded_data)

                exists = any(new_data[2] in row for row in loaded_data)

                if exists:
                    print("this code has been used")
                    await send_to("client1", "this code has been used")


                else:
                    try:
                        with open("data1.json", "r") as f:
                            data = json.load(f)
                    except (FileNotFoundError, json.JSONDecodeError):
                        data = [["start1"]]  

                    data.append(new_data)

                    with open("data1.json", "w") as f:
                        json.dump(data, f, indent=4)  
                    decode_data=new_data[2][0]
                    if decode_data=="1":
                        Mojito = item["Mojito"]
                        await send_to("client1", Mojito)
                    if decode_data=="2":
                        GinTonic = item["GinTonic"]
                        await send_to("client1",GinTonic)
                    if decode_data=="3":
                        WhiskeySour = item["WhiskeySour"]
                        await send_to("client1", WhiskeySour)

                    


                with open("data1.json", "r") as f:
                    loaded_data = json.load(f)
                print("loaded_data1:",loaded_data)




            elif new_data[1]=="client2":   ###
                try:
                    with open("data2.json", "r") as f:
                        data = json.load(f)
                except (FileNotFoundError, json.JSONDecodeError):
                    data = [["start2"]]  

                data.append(new_data)

                with open("data2.json", "w") as f:
                    json.dump(data, f, indent=4)  


                with open("data2.json", "r") as f:
                    loaded_data = json.load(f)
                print("loaded_data2:",loaded_data)

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
