import serial, socket, time
#import hashlib
import serial.tools.list_ports

from UsuarioDao import UsuarioDao
from Usuario import Usuario

#
#Escolher a porta do arduino
#
#Iniciando com 0 pois ainda não está conectado
arduino = 0

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

    try:
        if result is not None:        
            arduino.write('S'.encode())
            print("Sucesso")    
            #Inserir no registro o usuário que possui a senha digitada    
            inserirRegistro(result)
         
        else:
            #print("falha: {}".format(result[0]))
            arduino.write('F'.encode())
            print("Falha")
    except Exception as err:
        print("Ocorreu um erro no envio da mensagem", err)
        

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
        if (arduino):
            try:
                senha = int(arduino.readline().decode("UTF-8")[:-2])
            except Exception as err:
                senha = 0
                print("Ocorreu um erro com digitos recebidos: '", err)
            
            if senha:
                #Mostrar a senha para testes
                print(senha)       
                try:
                    logar(senha)                 
                except serial.serialutil.SerialException as err:
                    print("O dispositivo foi desconectado", err)
                    #Desconectando dispositivo
                    arduino = 0
                except Exception as err:
                    print("Ocorreu um erro ao tentar logar: '", err )
        else:
            #Tentar reconectar caso a conexão seja perdida        
            try:               
                #Escaneia todas as portas COM e procura uma com o nome de Arduino
                ports = list(serial.tools.list_ports.comports())
                for p in ports:
                    if "Arduino" in p.description:                       
                            print("Encontrado: ", p.description)
                            arduino = serial.Serial(p.device, 9600)                        
                            print("Conectado com sucesso")    
            #Caso não encontre, espere 30 segundos para tentar novametne         
            except Exception as err:            
                print("Porta serial inválida", err)
                print("Reconectando em 30 segundos...")
                arduino = 0
                time.sleep(30)
 
       




