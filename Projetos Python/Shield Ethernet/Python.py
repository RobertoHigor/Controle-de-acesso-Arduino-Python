import socket

IP = "192.168.20.2" 
PORTA = 65432 #Portas não registradas > 1023

#AF_INET é para Internet e SOCK_STREAM é para TCP
#with garante que caso ocorra um erro, ele irá automaticamente executar o método close() pois socket suporta context management.
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: 
    sock.bind((IP, PORTA)) #Associando o socket com o IP e Porta
    sock.listen() #Permite que o servidor aceite conexões, transformando em um socket de listening.
    #O accept() retorna 2 tuplas: Uma contendo o endereço da conexão (addr) e uma contendo um objeto socket representando a conexão (conn)
    conn, addr = sock.accept() #O processo fica suspenso aguardando uma conexão.

    try:
        with conn:
            print('Connected by', addr) #Nesse caso imprime o IP e a PORTA. Caso fosse conn, enviaria todos os dados relacionados ao socket como por ex o tipo (sock_stream)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data)
    except ConnectionResetError:
        print("Conexão com o Arduino perdida")
        sock.listen()
        conn, addr = sock.accept()

    #Lista de erros: ConnectionResetError = Foi forçado o caneclamento de uma conexão existente pelo host remoto