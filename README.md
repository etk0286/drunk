需安裝 pip install websockets
 

開啟程式後 terminal長這樣
PS C:\Users\etk02\Desktop\drunk> & C:/Users/etk02/anaconda3/python.exe c:/Users/etk02/Desktop/drunk/control_system.py
server IP: 10.100.4.177
WebSocket Server open ws://0.0.0.0:8765

client 端需與server連同個網路(內網通訊)

client 如app  url的部分是: ws://"server_ip":8765   ex:ws://10.100.4.177:8765

client 一連上須先發送 名稱id ,server端會抓取第一個接收到的訊息當作該client id

使用方式: 

連上後會顯示    terminal > [Server] ESP32_A Connected

全部字串傳輸 如app傳過來 server的terminal 會顯示 {"id" receive:傳輸內容}    如 [ESP32_A] receive: 123

如果要使用server傳輸訊息給指定client 指令格式為:id send 內容
如:send ESP32_A 123 
