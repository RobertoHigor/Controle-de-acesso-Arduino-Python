/*
  Programa com o código de comunicação do Arduino com o Python via socket.
  Responsável por autenticar no banco de dados o acesso do usuário e com isso liberar a porta.
  Autor: Roberto Higor Matos dos Anjos
*/

#include <Keypad.h>
#include <Ethernet.h>

// Variáveis do Arduino
#define LED 13
#define RELE A0 //Porta digital 6 PWM
#define BUZZER A1
#define SENHAMESTRE "l000001" //Apagar antes do commit
#define LEDVERMELHO  A3
#define LEDVERDE  A2
#define LIMITE_DE_ERROS 5

/*# Lista de salas #
# l = Laboratório de robótica
# d = Sala da diretora
# m = Manuntenção
# As salas com números serão as salas numeradas
        */
#define SALA 'l'

//Definindo as configurações da conexão
byte mac[] = { 0xBE, 0xAD, 0xBE, 0xEF, 0xFE, 0xED }; // MAC único. Gerador: https://ssl.crox.net/arduinomac/
byte ip[] = { 192, 168, 18, 34 }; // IP do Arduino 192.168.18.33 até 192.168.18.63
byte server[] = { 192, 168, 4, 23 }; // IP Do servidor.
int tcp_port = 65432; // Porta do servidor
EthernetClient client;

//Configuração do teclado
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

  //Pinos
  pinMode(RELE, OUTPUT);
  pinMode(BUZZER, OUTPUT);
  digitalWrite(RELE, HIGH); //Para começar com a porta fechada

  //Leds
  pinMode(LED, OUTPUT);
  pinMode(LEDVERMELHO, OUTPUT); //DECLARA O PINO COMO SAÍDA
  pinMode(LEDVERDE, OUTPUT); //DECLARA O PINO COMO SAÍDA
  digitalWrite(LEDVERMELHO, HIGH);// LED VERMELHO ACENDE
  digitalWrite(LEDVERDE, LOW);// LED VERDE APAGA

  //Esperar 1 segundo para inicializar o shield
  delay(1000);

  //Diminuindo o timeout do client.connect() para que não bloqueie o teclado
  client.setConnectionTimeout(100);
  conectar();

}

//Variaveis globais de contador
int contador = 0;
int contadorFalhas = 0;
char customKeyArray[10] = {};
char liberou = 0;

void loop(){

  //Reiniciar o contador se passar do numero máximo de dígitos.
  // Nesse caso Identificador da sala (1) + senha (6) + \o terminador (1) = (8 digitos)
  checarContadores();

  //Quando estiver recebendo dados. Entrar apenas caso esteja enviando uma senha
  if (client.available()){
        //Serial.println("Aguardando resposta...");
        char serialListener = client.read();

        if (liberou){
          if (serialListener == 'S'){
            piscarLED(1); //1 para sucesso
            liberarPorta();
            //Serial.println("Senha correta");
          }else if (serialListener == 'F'){  //Exibir falha caso receber um sinal 'F'
            piscarLED(2);
            //Serial.println("Senha inválida");
            contadorFalhas++;
          }
          liberou = 0;  //Impedir a entrada até limpar o Array
        }
  //Laço que o programa entra normalmente
  }else {
    char customKey = customKeypad.getKey(); //Pegar a tecla digitada
    //Adicionar somente digitos numéricos para o array

    if (customKey && isdigit(customKey)){
      //Caso for o primeiro dígito, adicionar o caractere identificador da sala
      if (contador == 0)
        customKeyArray[contador++] = SALA;
      customKeyArray[contador++] = customKey;
      tone(BUZZER, 400, 100);

      //Somente enviar caso tenha sido digitado 1 numero e apertado o * para finalizar
    //}else if (customKey == '*' && contador > 0){
      }else if (contador >= 7){
      customKeyArray[contador] = '\0'; //Terminador de String

      if (client.connected()){
        //Serial.println("Senha digitada: ");
        //Serial.println(customKeyArray);
        client.write(customKeyArray);
        liberou = 1; //Permite entrar no bloco para receber uma resposta
      }else if(!client.connected() && strcmp(customKeyArray, SENHAMESTRE) == 0){ //Caso o Arduino esteja desconectado
        piscarLED(1); //1 para sucesso
        liberarPorta();
        for(int i=0;i<4;i++) //SOM DE QUANDO LIBERA NO MODO OFFLINE
              tone(BUZZER,300,500);
      }else {
        piscarLED(2);
      }
      limparArray();
    }else if(customKey == '#'){
      tone(BUZZER,800,100);
      delay(100);
      tone(BUZZER,800,100);
      limparArray();
    }
  }

//Quando a conexão for perdida
  if (!client.connected()) {
      //Serial.println("Conexão perdida. Reconectando...");
      conectar();
  }
}

/**
* Métodos
**/
void conectar(){
  client.stop();
  //client.connect(server, tcp_port);
  Serial.println(Ethernet.localIP());
  if(client.connect(server, tcp_port)) {
    Serial.println("Conectado com o IP ");
    Serial.println(Ethernet.localIP());
  }
}

//Método para piscar LED no caso de sucesso ou falha
void piscarLED(char estado){
  switch(estado){
    //Sucesso
    case 1:
      digitalWrite(LEDVERDE, HIGH);
      digitalWrite(LEDVERMELHO, LOW);
      tone(BUZZER, 400, 500);
      delay(500);
      digitalWrite(LEDVERDE, LOW);
      digitalWrite(LEDVERMELHO, HIGH);
      break;
    //Falha
    case 2:
      for(int i=0;i<4;i++) //Som de senha inválida
        tone(BUZZER,300,200);

      for(int i=0;i<4;i++){  // Piscar LED Vermelho
        digitalWrite(LEDVERMELHO, LOW);  
        delay(300);
        digitalWrite(LEDVERMELHO, HIGH);
        delay(300);
      }
      digitalWrite(LEDVERMELHO, HIGH);
      break;
  }
}

void liberarPorta(){
  digitalWrite(RELE, LOW); //Liberar porta
  delay(1000);
  digitalWrite(RELE, HIGH); //Fechar porta
  contadorFalhas = 0;
  delay(2000); //Esperar 2 segundo para descansar.
}

void limparArray(){
  //Resetando o array e o contador
  customKeyArray[0] = '\0';
  contador = 0;
}

void checarContadores(){
  if (contador >=8){
      contador = 0;
  }
  if (contadorFalhas >= LIMITE_DE_ERROS){
      contadorFalhas = 0;
      delay(300000);
  }
}

