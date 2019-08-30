import serial
import time
import hashlib

from UsuarioDao import UsuarioDao
from Usuario import Usuario

#
#Escolher a porta do arduino
#
arduino = serial.Serial('COM3', 9600)

"""
    Métodos=================================
"""
#Método para checar senha
"""def criptografarSenha(senha):
    result = hashlib.sha256(senha.encode())
    return result.hexdigest()"""

#Inserir na tabela LOG quando a porta foi aberta
def inserirRegistro(result):
    usr = UsuarioDao()     
    usuarioRetorno = Usuario(result[0], result[1], result[4], result[5], result[6], result[7])               
    usr.inserirLog(usuarioRetorno)

#Método para chegar se achou um registro com a senha digitada
def logar(senha):
    usr = UsuarioDao()     
    #result = usr.logarUsuario(criptografarSenha(senha))
    result = usr.logarUsuario(senha)

    if result is not None:        
        arduino.write('S'.encode())
        print("Sucesso")    
        #Inserir no registro o usuário que possui a senha digitada    
        inserirRegistro(result)
         
    else:
        #print("falha: {}".format(result[0]))
        arduino.write('F'.encode())
        print("Falha")
        

"""
    Main ====================================
"""
#Instanciando as classes (teste senha 15158)
        #usuario1 = Usuario('Zuko Iroh', 'zukofire', senha)

        #Criar o banco de dados e inserir usuário
        #usr.criarBanco()
        #usr.inserirUsuario(usuario1)
while(1):  
        #Bloco para tratar erro nos digitos recebidos ao invés de parar o programa
        try:
            senha = int(arduino.readline().decode("UTF-8")[:-2])
        except Exception as err:
             senha = 0
             print("Ocorreu um erro com digitos recebidos: '", err)
        
        if senha:
            print(senha)       
            try:
                logar(senha) 
            except Exception as err:
                print("Ocorreu um erro no banco de dados: '", err )
 
       



