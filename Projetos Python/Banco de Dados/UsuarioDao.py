from ConnectionFactory import ConnectionFactory
import mysql.connector
from Usuario import Usuario
#exceptions https://codereview.stackexchange.com/questions/187951/crud-operations-for-a-contact-list-using-pymysql

#Classe responsável pelos querys no banco de dados
class UsuarioDao:  

    def criarBanco(self):
        try:
            con = ConnectionFactory.conectar()
            cursor = con.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Usuario (
                nome VARCHAR(50) NOT NULL,
                usuario VARCHAR(20) PRIMARY KEY,
                senha int(8) NOT NULL
                )""")
        except mysql.connector.Error as error:
            print("Falha ao criar o banco: {}".format(error))
        else:
            con.commit()
        finally:
            con.close()
            cursor.close()

    def inserirUsuario(self, novoUsuario):
        try:
            con = ConnectionFactory.conectar()
            cursor = con.cursor()

            cursor.execute("INSERT INTO livro VALUES (%s, %s, %s, %s) ", (novoUsuario.isbn, novoUsuario.titulo, novoUsuario.autor, novoUsuario.preco))                     
        #bloco de exceção
        except mysql.connector.Error as error:
            print("Falha ao inserir: {}".format(error))
        #bloco que será executado caso tudo ocorra bem
        else:
            con.commit()
        #bloco que sempre será executado para fechar a conexão
        finally:
            con.close()
            cursor.close()

    def selecionarUsuario(self, senha):
        try:
            con = ConnectionFactory.conectar()
            cursor = con.cursor()          
            #A variavel (senha,) precisa SEMPRE terminar em vírgula          
            cursor.execute("SELECT isbn FROM livro WHERE isbn = '%s'", (senha,))            
            
        except mysql.connector.Error as error:
            print("Failha ao obter o registro: {}".format(error))
        else:
            #return cursor.fetchall()
            return cursor.fetchone()
        finally:
            con.close()
            cursor.close()