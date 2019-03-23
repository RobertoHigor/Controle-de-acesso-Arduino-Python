//fonte https://gist.github.com/jreisstudio/4507236
#define LED 13

void setup() {
    pinMode(LED, OUTPUT);
    //To determine what serial port your Arduino is connected to look at the bottom right corner of your Arduino sketch
    Serial.begin(9600)
}

void loop() {
    if (Serial.avaialble()) {
        char serialListener = Serial.read();
        if (serialListener == 'H') {
            digitalWrite(LED, HIGH);
            Serial.write("Teste")
        }
        else if (SerialListener == 'L'){
            digitalWrite(LED, LOW);
        }
    }
}