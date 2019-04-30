
import serial
import time

arduino = serial.Serial('COM4', 9600)
"""
    Métodos ========================================
"""
def ligarDesligar():
    #Loop infinito para ficar recebendo mensagens
    #conseguir checar se chegou uma mensagem e imprimir ela  
    #while 1:
        #Um IF caso a mensagem seja "123", para imprimir alguma coisa
        arduino.write('A'.encode())
        data = arduino.readline().decode("UTF-8")[:-2]
        if data:
            print("Chegou a mensagem")
            print(data)
            arduino.write('A'.encode())
            if data == "123":
                print("Entrou no if 123")               
            ligarDesligar()
        else: 
            print("Não recebeu")
            ligarDesligar()
   
    
    #e enviar uma mensagem de volta para o arduino
"""
    Main =============================================
"""
time.sleep(2) #Esperar a inicialização
ligarDesligar()