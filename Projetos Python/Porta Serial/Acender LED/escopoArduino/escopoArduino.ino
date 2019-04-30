#include <Keypad.h>
#define LED 13
const byte ROWS = 4; 
const byte COLS = 4; 

char hexaKeys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

byte rowPins[ROWS] = {9, 8, 7, 6}; 
byte colPins[COLS] = {5, 4, 3, 2};

Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

void setup(){
  pinMode(LED, OUTPUT);
  Serial.begin(9600);  
}

int contador = 0;
char customKeyArray[10] = {};
char liberou = 0;

void loop(){
  if (Serial.available()){
    if (liberou){  
      char serialListener = Serial.read();     
      if (serialListener == 'S'){
        digitalWrite(LED, HIGH); 
        //delay(1000);
        //digitalWrite(LED, LOW); 
        liberou = 0;            
      }
      if (serialListener == 'F'){
        digitalWrite(LED, LOW);
        //delay(1000);
        //digitalWrite(LED, HIGH);
        liberou = 0;
      }      
    }
  }

  //Pegar uma tecla
  char customKey = customKeypad.getKey();  
  if (customKey){
    customKeyArray[contador++] = customKey;
  }

  //Imprimir caso a tecla seja *
  if (customKey == '*'){
    customKeyArray[contador-1] = '\0';
    Serial.println(customKeyArray);
    customKeyArray[0] = '\0';
    contador = 0;    
    liberou = 1; //Pode fazer a leitura do serial Listener    
  }

  
}
