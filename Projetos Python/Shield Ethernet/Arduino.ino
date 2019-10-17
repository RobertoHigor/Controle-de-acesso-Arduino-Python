#include <Ethernet.h>
#include <SPI.h>

byte mac[] = { 0xBE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
byte ip[] = { 192, 168, 20, 100 };
byte server[] = { 192, 168, 20, 2 }; // Touchberry Pi Server
int tcp_port = 65432;

EthernetClient client;

void setup()
{
  Ethernet.begin(mac, ip);
  Serial.begin(9600);

  delay(1000);

  Serial.println("Connecting...");

  if (client.connect(server, tcp_port)) { // Connection to server.js
    Serial.println("Connected to server.js");
    client.println();
  } else {
    Serial.println("connection failed");
  }
}

void loop()
{
  if (client.available()) {
    if(Serial.available()){
      char s = Serial.read();
      client.write(s); // Send what is reed on serial monitor
      char c = client.read();
      Serial.print(c); // Print on serial monitor the data from server 
    }
  }

  if (!client.connected()) {
    Serial.println();
    Serial.println("disconnecting.");
    client.stop();
    for(;;)
      ;
  }
}