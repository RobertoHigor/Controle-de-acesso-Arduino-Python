#include <LiquidCrystal.h>
#include <Servo.h>

#define SERVO 3 // Porta Digital 6 PWM

Servo s; // Variável Servo
int pos; // Posição Servo







//#include <Key.h>                //borrar si causa algunos problemas en compilación          
//#include <Keypad.h>
int M1 = 2;
bool M1state = false;
int a=0, b=0, c=0, d=0;//acumuladores de datos enteros para la contrseña.
int var=0; //incremento apara el switch.
String key;//contraseña....Ustedes pueden codificarlo la contraseña
char f='*';  //caracter para cubrir la contraseña.
int veces=0,incorrecto=0; //seguridad de solo 3 intentos para ingresar la contraseña correcta.
int aviso=3; //aviso para mostrar los intentos como seguridad para el usuario.
String readString;
/*
const byte filas = 4; //cuatro  filas.
const byte columnas = 4; //cuatro columnas.
char tecla[filas][columnas] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'*','0','#','D'}
};
byte pinFilas[filas] = {7, 6, 5, 4}; //conectarse a las patillas de salida de fila del teclado.
byte pinColumnas[columnas] = {3, 2, A4, A5}; //conectarse a las patillas de las columnas del teclado.

Keypad keypad = Keypad( makeKeymap(tecla), pinFilas, pinColumnas, filas, columnas );
LiquidCrystal lcd(13,12,11,10,9,8); //RS,E,D4,D5,D6,D7
*/

void serialRead() { 
  while (Serial.available()) {
  delay(10);  
  if (Serial.available() >0) {
    char c = Serial.read();
    readString += c;}
  }
}

void setup(){
  //lcd.begin(16,2); //LCD (16 COLUMNAS Y 2 FILAS)
  s.attach(SERVO);
  Serial.begin(9600);
  s.write(90); 
  pinMode(A0,OUTPUT); //TRUE PASSWORD CORRECTO LED YELLOW.
  pinMode(A1,OUTPUT); //FALSE PASSWORD INCORRECTO LED RED.
  pinMode(M1, OUTPUT);
  key="1234";
}
  
void loop(){
  String password, npassword;
  if(Serial.available()> 0){
    readString = "";
    serialRead();
    password = readString.substring(0,4);
    if(password.startsWith("mmmm")){
       Serial.print("Senha atual: ");
       Serial.print(key[0]);
       Serial.print(key[1]);
       Serial.print(key[2]);
       Serial.println(key[3]);
    }
    else if(password.startsWith("ssss")){
      Serial.println("digite a nova senha: ");
      readString = "";
       while(readString==""){
       if(Serial.available()>0){
         serialRead();
         npassword = readString.substring(0,4);
         key=npassword;
         Serial.println("Senha alterada!");
        }
      }
      //Serial.println("caiu aqui: "); 
    }
    else{
   delay(100);
  if(password.startsWith(key)){
    //lcd.clear();
    //lcd.setCursor(3,0);
    //lcd.print("Senha");
    //lcd.setCursor(3,1);
    //lcd.print("correta");
    Serial.print("Senha: ");
    Serial.println(password);
    Serial.println("Senha correta");
    digitalWrite(A0,HIGH);
    if(M1state==false){
       s.write(0);
       M1state=true;
    }
    else{
       s.write(90);
       M1state=false;
    }
    delay(700);
    //lcd.clear();
    digitalWrite(A0,LOW);
    veces=0;//si es correcto el password ,variable veces no se incremeta.
    aviso=3;//variable aviso se mantiene en 3
    }
  else{
    //lcd.clear();
    //lcd.setCursor(3,0);
    //lcd.print("Senha");
    //lcd.setCursor(3,1);
    //lcd.print("errada");
    Serial.print("Senha: ");
    Serial.println(password);
    Serial.println("Senha incorreta");
    digitalWrite(A1,HIGH);
    delay(400);
    //lcd.clear();
    digitalWrite(A1,LOW);
      veces ++; //incrementamos los intentos incorrectos de password para el bloqueo.
      aviso --; //decremento de variable aviso ,de 3 hasta 0 según las veces de fallas al ingresar el password.
      //lcd.setCursor(2,0);
      Serial.print("Restam ");
      Serial.print(aviso);
      Serial.println(" tentativas");
      //lcd.print("Restam: ");
      //lcd.setCursor(13,0);
      //lcd.print(aviso);
      //lcd.setCursor(2,1);
      //lcd.print("tentativas");
       if(aviso==0){
         Serial.println("Alarme ativado");
          //lcd.clear();
          //lcd.setCursor(5,0);
          //lcd.print("ALARMA");
          //lcd.setCursor(4,1);
          //lcd.print("ACTIVADO");
        }
      delay(300);//lcd.clear();
    }
//------Seguridad para la contraseña y sus restricciones-------------------//

  while(veces>=3){
      //lcd.setCursor(1,0),lcd.print("Alerta Policia");
      //lcd.setCursor(4,1),lcd.print("Intrusos");
      digitalWrite(A1,HIGH);
      delay(100);
      ///lcd.clear();
      digitalWrite(A1,LOW);delay(50);
  }//while es Bucle infinito de seguridad para bloquear los re intentos del password

   var=0;
   //lcd.clear();
    }
  }
 if(!password){//lcd.setCursor(0,0),lcd.print("Digite a senha");}//portada de inicio en el LCD
  //Serial.println("Digite a senha: ");
 }
  delay(2);
}
