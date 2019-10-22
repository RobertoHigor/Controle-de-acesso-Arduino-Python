#pip install psycopg2
import psycopg2
from psycopg2 import Error

class ConnectionFactory:
    #Metodo estático parar poder usar sem instanciar a classe
    @staticmethod
    def conectar():
        try:
            con = psycopg2.connect(
            host="localhost",
            user="postgres",
            password="26793653",
            database="faeterj"
            )
        #Mensagem de erro
        except (Exception, psycopg2.Error) as error:
            print('Ocorreu um erro com o banco de dados: {}, valor {!r}'.format(error.args[0], error))
            raise
        #Retorna o objeto con caso ocorra tudo bem
        else:
            return con
        #cursor = con.cursor()
        #cursor.execute(query)

   
   

