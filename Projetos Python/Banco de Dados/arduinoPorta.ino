#include <Keypad.h>

#include <Keypad.h>

#define LED 13
#define RELE 11 //Porta digital 6 PWM

//Exemplo:
//http://wiring.org.co/reference/libraries/Keypad/Keypad_addEventListener_.html

const byte ROWS = 4; 
const byte COLS = 3; 

char hexaKeys[ROWS][COLS] = {
  {'1', '2', '3'},
  {'4', '5', '6'},
  {'7', '8', '9'},
  {'*', '0', '#'}
};

//byte rowPins[ROWS] = {9, 8, 7, 6}; 
//byte colPins[COLS] = {5, 4, 3}; 

byte rowPins[ROWS] = {8, 7, 6, 9}; 
byte colPins[COLS] = {5, 4, 3, 2};

Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

void setup(){
  Serial.begin(9600);  
  pinMode(LED, OUTPUT); 
  pinMode(RELE, OUTPUT);   //(ver se é output) 
}

int contador = 0;
char customKeyArray[10] = {};
char liberou = 0;

void loop(){

if (contador >=9){    
    contador = 0;
}

if (Serial.available()){
    if (liberou){  
        char serialListener = Serial.read();     
        if (serialListener == 'S'){
            digitalWrite(LED, HIGH); 
            digitalWrite(RELE, LOW);
            delay(1000);
            digitalWrite(LED, LOW); 
            //digitalWrite(RELE, HIGH);
            liberou = 0;            
        }
        if (serialListener == 'F'){           
            liberou = 0;
        }      
    }
}

  //Pegar uma tecla
  char customKey = customKeypad.getKey(); 
  //Ignorar a tecla "*" 
  if (customKey && customKey != '*'){
    customKeyArray[contador++] = customKey;
  }

  //Imprimir caso a tecla seja *
  /*
        Implementar um sistema pro contador resetar. O fato de adicioanr um \0 no final já resolve o problema de memória.
        "Coloquei o contador para resetar para impedir qcom que o programa parasse de funcionar por estouro de memória"

  */
  //Somente enviar caso tenha sido digitado 1 numero
  if (customKey == '*' && contador > 0){
    customKeyArray[contador] = '\0';
    Serial.println(customKeyArray);
    customKeyArray[0] = '\0';
    contador = 0;    
    liberou = 1; //Pode fazer a leitura do serial Listener    
  }

delay(100);
  
}