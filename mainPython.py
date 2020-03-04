"""
Programa principal responsável por executar a aplicação desktop Python. Ela serve para autenticar no banco de dados o acesso recebido do Arduino além de gravar o registro do mesmo.
Autor: Roberto Higor Matos dos Anjos
"""
import serial, socket, time, select, queue

from UsuarioDao import UsuarioDao
from Usuario import Usuario

"""
    Variáveis
"""

IP = "192.168.4.23" #Ip do servidor. "" significa todos os ips do computador (local e de rede)
PORTA = 65432 #Portas não registradas > 1023
TIMEOUT = 900 #Tempo esperando por dados

"""
    Métodos=================================
"""

#Inserir na tabela LOG quando a porta foi aberta
def inserirRegistro(result, sala):  
    usr = UsuarioDao()
    usuarioRetorno = Usuario(result[0], result[1], result[4], result[5], result[6], result[7])   
    usr.inserirLog(usuarioRetorno, sala)

#Método para chegar se achou um registro com a senha digitada
def logar(s, senha, sala):
    usr = UsuarioDao()
    result = usr.logarUsuario(senha, sala)
    try:        
        if result is not None:        
            message_queues[s].put('S'.encode())
            print("Sucesso na sala {}".format(sala))    
            #Inserir no registro o usuário que possui a senha digitada    
            inserirRegistro(result, sala)            
        
        else:            
            message_queues[s].put('F'.encode())
            print("Falha na sala {}".format(sala))
    except Exception as err:
        print("Ocorreu um erro no envio da mensagem", err)          

"""
    Main ====================================
"""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Serve para criar um socket non-blocking, não bloqueando o sistema e permitindo mais de um cliente.
server.setblocking(0)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Permitir reutilizar um socket aberto
server.bind(('localhost', PORTA))  
print("Bind no IP: {} e PORTA: {}".format(IP, PORTA))
print("Servidor ouvindo...") 

server.listen(20) #Numero de conexões aceitas
inputs = [server] #São os sockets onde será lido os dados
outputs = []#São os sockets em será escrito
message_queues = {}# Dicionario de mensagens

while(1):  
        # Bloco para tratar erro nos digitos recebidos ao invés de parar o programa
        if inputs: 
            readable, writable, exceptional = select.select(inputs, outputs, inputs)          

            #                                 
            # Lidar com os sockets que enviaram dados
            #
            for s in readable:
                # Se o socket em input for um server, significa então que chegou um novo cliente.
                # Deve-se abrir uma nova conexão com o accept()
                if s is server:
                    connection, client_address = s.accept()
                    print("Nova conexão de {}".format(client_address))
                    # Deixando a conexão como non-blocking para não suspender o sistema
                    connection.setblocking(0)

                    # Adiciona o novo cliente para a lista de inputs e cria uma fila de mensagens
                    inputs.append(connection)
                    message_queues[connection] = queue.Queue()
                # Senão, significa que é um cliente existente que possui dados
                else:
                    try:
                        # @@@@@@@@ Testar se precisa do send b'1' para checar conexão
                        data = s.recv(7).decode("UTF-8") #decode serve para transformar em caracteres e o :-2 significa ir até -2 para cortar \n
                        senha = int(data[1:])
                        sala = data[:1]               
                        if data:
                            print("Recebido {} de {}".format(data, s.getpeername()))          
                            # Autenticar a snah recebida
                            try:
                                logar(s, senha, sala)    
                            except OSError as err:
                                print("Ocorreu um erro com o Socket", err)                        
                            except Exception as err:
                                print("Ocorreu um erro ao tentar logar: '", err )
                        # Adicionar em outputs para ser escrito posteriormente (writable)      
                            if s not in outputs:
                                    outputs.append(s)                        

                        # Um socket readable sem dados significa que o cliente se desconectou
                        else:
                            # Interpretar um resultado vazio como uma conxão fechada
                            print("Fechando {} após ler dados vazios".format(client_address))
                            # Remover então de outputs caso exista e em seguida de inputs
                            if s in outputs:
                                outputs.remove(s)
                            inputs.remove(s)
                            # Após removido do Array do select, pode-se fechar a conexão e remover as mensagens
                            s.close()
                            del message_queues[s]

                    except socket.timeout as err:
                        print("Sem dados recebidos: ", err)       
                    except socket.error as err:
                        # O programa trava em caso de erro no Socket. 
                        # O erro então é tratado nesse exception que faz a mesma tarefa do exceptional
                        # Removendo o socket das listas e o fechando
                        print("Erro na conexão ao receber os dados: ", err)  
                        inputs.remove(s)
                        if s in outputs:
                            outputs.remove(s)
                        s.close()
                    except ValueError as err:
                        senha = 0
                        print("Ocorreu um erro com digitos recebidos: '", err) 
                    except Exception as err:
                        senha = 0
                        print("Ocorreu um erro com digitos recebidos: '", err)  
                        
            #
            #Pega as mensagens pendentes e as escreve no socket
            #
            for s in writable:
                try:
                    next_msg = message_queues[s].get_nowait()
                #Caso ocorra algum erro, ele será removido da lista de sockets.
                except queue.Empty:
                    # Não há mais mensagens na fila. Remover da lista de Writable.
                    print("Fila output do {} está vazia".format(s.getpeername()))
                    outputs.remove(s)
                else:
                    print("Enviando {} para {}".format(next_msg, s.getpeername()))
                    s.send(next_msg)
            # Quando há algum erro com o socket
            for s in exceptional:
                print("Tratando exception de {}".format(s.getpeername()))
                # Parar de esperar inputs na conexão
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()

                # Remover fila de mensagens
                del message_queues[s]
                        
                    
    




