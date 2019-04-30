#fonte https://gist.github.com/jreisstudio/4507236
#https://stackoverflow.com/questions/24074914/python-to-arduino-serial-read-write
import serial
import time

#Replace Serial.readString() with Serial.readStringUntil('\n'), the former returns when it times out, whereas the latter returns when it matches a newline character or it times out. The default timeout is 1 second.

#configurar a porta serial do arduino
#To determine what serial port your Arduino is connected to look at the bottom right corner of your Arduino sketch
arduino = serial.Serial('COM4', 9600)

#Método para enviar um caractere para ligar ou desligar LED
def ligarDesligar():
    comando = input("Digite alguma coisa..: (on/ off/ bye): ")
    if comando == "on":
        print("O led está ligado...")
        time.sleep(1)
        #Tem que utilizar o encode() pois o arduino não aceita strings UNICODE.
        arduino.write('H'.encode())
        time.sleep(1)
        #.decode() serve para tirar o prefixo b ' ' que indica que é uma rray de bytes.
        #Como altenativa, poderia utilizar na variável: data.decode("UTF-8")
        data = arduino.readline()[:-2].decode("utf-8") #the last bit gets rid of the new-line 
        if data:     
            print(data) 
        #https://stackoverflow.com/questions/37804315/reading-integer-from-arduino-using-pyserial
        ligarDesligar()
    elif comando == "off":
        print("O led está desligado...")
        time.sleep(1)
        arduino.write('L'.encode())   
        time.sleep(1)     
        data = arduino.readline()[:-2].decode("utf-8") #the last bit gets rid of the new-line chars
        if data:            
            print(data)    
        ligarDesligar()
    elif comando == "bye":
        print("Até logo...")
        time.sleep(1)
        arduino.write('O'.encode())
        time.sleep(1)
        data = arduino.readline()[:-2].decode("utf-8")
        if data:
            print(data)
        arduino.close()
    else:
        print("Digite apenas on, off ou bye")
        ligarDesligar()

time.sleep(2) #Esperar a inicialização
ligarDesligar()