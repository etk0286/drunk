#include <WiFi.h>
#include <WebSocketsClient.h>

const char* ssid     = "ASUS_88";
const char* password = "efg60624";

const char* host = "192.168.50.197";  // Python server IP
const uint16_t port = 8765;

WebSocketsClient webSocket;

// ⚡ 每台機器給自己一個 ID
String client_id = "ESP32_A";

void webSocketEvent(WStype_t type, uint8_t * payload, size_t length) {
  switch(type) {
    case WStype_CONNECTED:
      Serial.println("[WebSocket] 已連線!");
      // 連上後馬上把 ID 傳給 server
      webSocket.sendTXT(client_id);
      break;

    case WStype_DISCONNECTED:
      Serial.println("[WebSocket] 已斷線，嘗試重連...");
      break;

    case WStype_TEXT:
      Serial.printf("[Server 指令] %s\n", (char*)payload);
      // TODO: 可以根據訊息控制馬達或其他裝置
      break;
  }
}

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" WiFi 已連上");

  webSocket.begin(host, port, "/");
  webSocket.onEvent(webSocketEvent);
  webSocket.setReconnectInterval(5000);  // 斷線 5 秒後自動重連
}

void loop() {
  webSocket.loop();

  // 從 Serial Monitor 手動輸入 -> 傳到 server
  if (Serial.available() > 0) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();
    if (msg.length() > 0) {
      webSocket.sendTXT(msg);
      Serial.printf("[WS] 發送: %s\n", msg.c_str());
    }
  }
}
