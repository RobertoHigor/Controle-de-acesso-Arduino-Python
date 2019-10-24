import serial, socket, time

from UsuarioDao import UsuarioDao
from Usuario import Usuario

"""
    Variáveis
"""

IP = "192.168.0.171" #Ip do servidor. "" significa todos os ips do computador (local e de rede)
PORTA = 65432 #Portas não registradas > 1023
TIMEOUT = 1800 #Tempo esperando por dados

"""
    Métodos=================================
"""

#Inserir na tabela LOG quando a porta foi aberta
def inserirRegistro(result):
    usr = UsuarioDao()     
    usuarioRetorno = Usuario(result[0], result[1], result[4], result[5], result[6], result[7])             
    usr.inserirLog(usuarioRetorno)
    

#Método para chegar se achou um registro com a senha digitada
def logar(senha):
    usr = UsuarioDao()     
    result = usr.logarUsuario(senha)

    try:
        if result is not None:           
            conn.sendall('S'.encode())
            print("Sucesso")    
            #Inserir no registro o usuário que possui a senha digitada    
            inserirRegistro(result)
         
        else:
            #print("falha: {}".format(result[0]))
            conn.sendall('F'.encode())
            print("Falha")
    except Exception as err:
        print("Ocorreu um erro no envio da mensagem", err)          

"""
    Main ====================================
"""
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    print("Bind no IP: {} e PORTA: {}".format(IP, PORTA))
    sock.bind((IP, PORTA))  
    print("Servidor ouvindo...") 
    sock.listen()

    conn, addr = sock.accept()
    conn.setblocking(False)
    conn.settimeout(TIMEOUT)
    print("Conexão de {} aceita".format(addr))

    while(1):  
            #Bloco para tratar erro nos digitos recebidos ao invés de parar o programa
            if(conn):                                            
                try:
                    print("Aguardando dados...")   
                    conn.send(b'1')                                  
                    senha = int(conn.recv(8).decode("UTF-8")) #decode serve para transformar em caracteres e o :-2 significa ir até -2 para cortar \n                     
                    #Parar caso não receber mais dados
                    if not senha: 
                        print("Conexão perdida, sem mais dados")
                        conn = 0
                    elif senha:
                        #Mostrar a senha para testes
                        print(senha)            
                        try:
                            logar(senha)    
                        except OSError as err:
                            print("Ocorreu um erro com o Socket", err)                           
                        except Exception as err:
                            print("Ocorreu um erro ao tentar logar: '", err )
                                                                      
                except socket.timeout as err:
                    print("Sem dados recebidos: ", err)                      
                                  
                except socket.error as err:
                    print("Erro na conexão: ", err)      
                    conn = 0                       
                except Exception as err:
                    senha = 0
                    print("Ocorreu um erro com digitos recebidos: '", err)                    
                
            else:
                #Tentar reconectar caso a conexão seja perdida                 
                print("Reconectando...")                                               
                try:              
                    #Reiniciando servidor
                    sock.listen()
                    conn, addr = sock.accept()
                    conn.setblocking(False)
                    conn.settimeout(TIMEOUT)
                    print("Conectado com sucesso")    
                #Caso não encontre, espere 30 segundos para tentar novametne         
                except Exception as err:            
                    print("Conexão perdida", err)
                    print("Reconectando em 30 segundos...")                
                    time.sleep(30)
 
       




