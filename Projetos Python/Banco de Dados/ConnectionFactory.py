import mysql.connector

class ConnectionFactory:
    #Metodo estático parar poder usar sem instanciar a classe
    @staticmethod
    def conectar():
        try:
            con = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="26793653",
            database="demoapi"
            )
        #Mensagem de erro
        except mysql.connector.Error as error:
            print('Exceção número: {}, valor {!r}'.format(error.args[0], error))
            raise
        #Retorna o objeto con caso ocorra tudo bem
        else:
            return con
        #cursor = con.cursor()
        #cursor.execute(query)

   
   

