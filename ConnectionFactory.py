#pip install psycopg2
import psycopg2
from psycopg2 import Error
imoprt os

class ConnectionFactory:
    #Metodo estático parar poder usar sem instanciar a classe
    @staticmethod
    def conectar():
        try:
            con = psycopg2.connect(
            host="localhost",
            user="postgres",
            password=os.environ['DB_PASS'],
            database="faeterj"
            )
        #Mensagem de erro
        except (Exception, psycopg2.Error) as error:
            print('Exceção número: {}, valor {!r}'.format(error.args[0], error))
            raise
        #Retorna o objeto con caso ocorra tudo bem
        else:
            return con
        #cursor = con.cursor()
        #cursor.execute(query)

   
   

