/*
  Programa com o código de comunicação do Arduino com o Python via socket.
  Responsável por autenticar no banco de dados o acesso do usuário e com isso liberar a porta.
  Autor: Roberto Higor Matos dos Anjos
*/

#include <Keypad.h>
#include <Ethernet.h>

#define LED 13
#define RELE A0 //Porta digital 6 PWM
#define BUZZER A1
#define SENHAMESTRE "INSERIR SENHA MASTER AQUI" //Apagar antes do commit

//Definindo as configurações da conexão
byte mac[] = { 0xBE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED };
byte ip[] = { 192, 168, 0, 200 };
byte server[] = { 192, 168, 0, 171 }; // Touchberry Pi Server
int tcp_port = 65432;
EthernetClient client;

//Configuração de teclado
const byte ROWS = 4; 
const byte COLS = 4; 

char hexaKeys[ROWS][COLS] = {
  {'1', '2', '3', 'A'},
  {'4', '5', '6', 'B'},
  {'7', '8', '9', 'C'},
  {'*', '0', '#', 'D'}
};

//Ordem dos pinos
byte rowPins[ROWS] = {9, 8, 7, 6}; 
byte colPins[COLS] = {5, 3, 2, 1};

Keypad customKeypad = Keypad(makeKeymap(hexaKeys), rowPins, colPins, ROWS, COLS); 

void setup(){
  //Inicializando a conexão com o mac e ip definidos.
  Ethernet.begin(mac, ip);
  Serial.begin(9600);  
  pinMode(LED, OUTPUT); 
  pinMode(RELE, OUTPUT); 
  pinMode(BUZZER, OUTPUT);  
  digitalWrite(RELE, HIGH); //Para começar com a porta fechada

  //Um segundo para o shield inicializar
  delay(1000);
  //Diminuindo o timeout do client.connect() para que não bloqueie o Arduino
  client.setConnectionTimeout(100);
  conectar();
  
}

int contador = 0;
char customKeyArray[10] = {};
char liberou = 0;

void loop(){

//Reiniciar o contador se passar do numero máximo de dígitos.
if (contador >=7){    
    contador = 0;
}

//Quando estiver recebendo dados. Entrar apenas caso esteja enviando uma senha
if (client.available()){ 
        Serial.println("Aguardando resposta...");
        char serialListener = client.read(); 
        //Liberar caso receber um sinal 'S'    
        if (serialListener == '1'){
          //fazer nada. Testar sem else if caso dê erro.
        }else if (liberou){
          if (serialListener == 'S'){ 
          tone(BUZZER, 400, 500);          
          digitalWrite(RELE, LOW); //Liberar porta
          delay(1000);           
          digitalWrite(RELE, HIGH); //Fechar porta
          liberou = 0;  //Impedir de entrar novamente nesse bloco até limpar o array   
          Serial.println("Senha correta");       
          delay(2000); //Esperar 2 segundo para descansar.
        }else if (serialListener == 'F'){  //Exibir falha caso receber um sinal 'F'
          Serial.println("Senha inválida");
          for(int i=0;i<4;i++){ //SOM DE ERRO QUANDO A SENHA DIGITADA ESTÁ INCORRETA
            tone(BUZZER,300,200);     
          liberou = 0;
        }   
        }                   
}else {
  //Pegar a tecla digitada
  char customKey = customKeypad.getKey(); 
  //Adicionar somente digitos numéricos para o array
  if (customKey && isdigit(customKey)){
    //Serial.println(customKey);
    customKeyArray[contador++] = customKey;
    tone(BUZZER, 400, 100);
  }else if (customKey == '*' && contador > 0){ //Somente enviar caso tenha sido digitado 1 numero e apertado o * para finalizar
    //Colocando um terminador de string
    customKeyArray[contador] = '\0';
    Serial.println("Senha digitada: ");
    Serial.println(customKeyArray);
    client.write(customKeyArray);

    //Lembrar de esconder a senha mestre @@@@@@@@@@@@
    if(!client.connected() && strcmp(customKeyArray, SENHAMESTRE) == 0){      
      Serial.println("Utilizando liberação no modo offline");
      for(int i=0;i<4;i++){ //SOM DE QUANDO LIBERA NO MODO OFFLINE
            tone(BUZZER,300,500); 
      digitalWrite(RELE, LOW); //Liberar porta
      delay(1000);           
      digitalWrite(RELE, HIGH); //Fechar porta
    }
  
    //Resetando o array e o contador
    customKeyArray[0] = '\0';
    contador = 0;    
    liberou = 1; //Permite entrar no bloco para receber uma resposta   
  }    
}

//Quando a conexão for perdida
if (!client.connected()) {
    //Serial.println("Conexão perdida. Reconectando..."); 
    conectar();
  }
}

void conectar(){
  client.stop();
  if(client.connect(server, tcp_port)) {
    Serial.println("Conectado no ConectarUmaVez");
  }
}