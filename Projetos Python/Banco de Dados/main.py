import serial
import time

from UsuarioDao import UsuarioDao
from Usuario import Usuario

"""
    Métodos=================================
"""
#Método para chegar se achou um registro com a senha digitada
def logar(resultado):
    print(resultado)
    if result is not None:
        #print("sucesso: {}".format(result[0]))
        print("Sucesso")
    else:
        #print("falha: {}".format(result[0]))
        print("Falha")

"""
    Main ====================================
"""
#arduino = serial.Serial('/dev/tty.usbmodem1411', 9600)

#Instanciando as classes
usuario1 = Usuario('Zuko Iroh', 'zukofire', 15158)
usr = UsuarioDao()

#Criar o banco de dados e inserir usuário
#usr.criarBanco()
#usr.inserirUsuario(usuario1)

result = usr.selecionarUsuario(usuario1)
logar(result)

