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
                usuario VARCHAR(20),
                senha int(8)
                PRIMARY KEY(usuario, senha)
                )""")

            """
            Importante:
                Não pode ser permitido repetir asenha, podendo ser ela uma chave primária
            """
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
            
            #cursor.execute("INSERT INTO livro VALUES (%s, %s, %s, %s) ", (novoUsuario.isbn, novoUsuario.titulo, novoUsuario.autor, novoUsuario.preco))   
            cursor.execute("INSERT INTO Usuario VALUES (%s, %s, %s)", (novoUsuario.nome, novoUsuario.usuario, novoUsuario.senha))                  
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

    def inserirLog(self, usuarioLogin):
        try:
            con = ConnectionFactory.conectar()
            cursor = con.cursor()            
            cursor.execute("INSERT INTO log (usuario_id, sala) VALUES (%s, 'Sala 4')", (usuarioLogin.usuario,))
        except mysql.connector.Error as error:        
            print("Falha ao inserir o registro: {}".format(error))
        else:
            con.commit()
        finally:
            con.close()
            cursor.close()

    def selecionarUsuario(self, usuarioConsulta):
        try:
            con = ConnectionFactory.conectar()
            cursor = con.cursor()          
            #A variavel (senha,) precisa SEMPRE terminar em vírgula          
            cursor.execute("SELECT * FROM Usuario WHERE senha = '%s'", (usuarioConsulta.senha,))            
            
        except mysql.connector.Error as error:
            print("Falha ao obter o registro: {}".format(error))
        else:
            #return cursor.fetchall()
            return cursor.fetchone()
        finally:
            con.close()
            cursor.close()

    def logarUsuario(self, senha):
        try:
            con = ConnectionFactory.conectar()
            cursor = con.cursor()          
            #A variavel (senha,) precisa SEMPRE terminar em vírgula          
            cursor.execute("SELECT * FROM Usuario WHERE senha = '%s'", (senha,))            
            
        except mysql.connector.Error as error:
            print("Falha ao obter o registro: {}".format(error))
        else:
            return cursor.fetchone()                                 
        finally:
            con.close()
            cursor.close()