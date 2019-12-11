import select, socket, sys, queue

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Serve para criar um socket non-blocking, não bloqueando o sistema e permitindo mais de um cliente.
server.setblocking(0)
print("Iniciando o servidor")
server.bind(('localhost', 50000))

server.listen(5)
inputs = [server]
outputs = []
message_queues = {}

while inputs:
    # O select pergunta ao OS se o socket é readable, writable ou se houve alguma exceção.
    # Este método ira bloquear o sistema até que algum socket esteja pronto.
    #print("Esperando pelo próximo evento")
    readable, writable, exceptional = select.select(inputs, outputs, inputs)
    
    for s in readable:
        # Se tem um server socket em inputs, significa que chegou um novo cliente. Então deve-se utilizar o accept()
        if s is server:
            connection, client_address = s.accept()
            print("Nova conexão de {}".format(client_address))
            connection.setblocking(0)
            #Adiciona o novo socket para lista de inputs e cria uma fila para as mensagens que serão enviadas de volta
            inputs.append(connection)
            message_queues[connection] = queue.Queue()        
        else:
            data = s.recv(1024)
            #Um socket readable tem dados
            if data:
                print("Recebido {} de {}".format(data, s.getpeername()))
                message_queues[s].put(data)
                if s not in outputs:
                    outputs.append(s)
                # Um socket readable sem dados é de um cliente que se desconectou
            else:
                # Interpretar um resultado vazio como uma conexão fechada
                print("Fechando {} após ler dados vazios".format(client_address))
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()

                # Remover fila de mensagens
                del message_queues[s]
    #Pega as mensagens pendentes e as escreve no socket
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