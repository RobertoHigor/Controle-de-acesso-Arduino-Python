#include <Keypad.h>

#define LED 13
#define RELE 11 //Porta digital 6 PWM

//Exemplo:
//http://wiring.org.co/reference/libraries/Keypad/Keypad_addEventListener_.html

const byte ROWS = 4; 
const byte COLS = 4; 

//Configuração de teclado da faculdade
char hexaKeys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

//Ordem dos pinos da faculdade
byte rowPins[ROWS] = {8, 7, 6, 9}; 
byte colPins[COLS] = {5, 4, 3, 2};

Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

void setup(){
  Serial.begin(9600);  
  pinMode(LED, OUTPUT); 
  pinMode(RELE, OUTPUT);   
  digitalWrite(RELE, HIGH); //Para começar com a porta fechada
}

int contador = 0;
char customKeyArray[10] = {};
char liberou = 0;

void loop(){

//Reiniciar o contador se passar do numero máximo
if (contador >=9){    
    contador = 0;
}

//Se a conexão serial estiver disponível
if (Serial.available()){
    if (liberou){  
        char serialListener = Serial.read(); 
        //Liberar caso receber um sinal 'S'    
        if (serialListener == 'S'){
            digitalWrite(LED, HIGH); //Acender LED
            digitalWrite(RELE, LOW); //Liberar porta
            delay(1000);
            digitalWrite(LED, LOW); //Apagar LED
            digitalWrite(RELE, HIGH); //Fechar porta
            liberou = 0;  //Impedir de entrar novamente nesse bloco até limpar o array          
        }
        //Exibir falha caso receber um sinal 'F'
        if (serialListener == 'F'){           
            liberou = 0;
        }      
    }
}

  //Pegar uma tecla
  char customKey = customKeypad.getKey(); 
  //Ignorar a tecla "*" 
  if (customKey && isdigit(customKey)){
    customKeyArray[contador++] = customKey;
  }
 
  /*
        Implementar um sistema pro contador resetar. O fato de adicioanr um \0 no final já resolve o problema de memória.
        "Coloquei o contador para resetar de forma a impedir qcom que o programa pare de funcionar caso ocorra estouro de memória"

  */
  //Imprimir caso a tecla seja *
  //Somente enviar caso tenha sido digitado 1 numero
  if (customKey == '*' && contador > 0){

    //Finalizando a linha para enviar o array
    customKeyArray[contador] = '\0';
    Serial.println(customKeyArray);

    //Resetando o array e o contador
    customKeyArray[0] = '\0';
    contador = 0;    
    liberou = 1; //Pode fazer a leitura do serial Listener    
  }

delay(100);
  
}
