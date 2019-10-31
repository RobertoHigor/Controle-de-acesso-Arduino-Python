from ConnectionFactory import ConnectionFactory
import psycopg2, os
from psycopg2 import Error
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
                Não pode ser permitido repetir a senha, podendo ser ela uma chave primária
            """
        except (Exception, psycopg2.Error) as error:
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
        
        except (Exception, psycopg2.Error) as error:
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
            cursor.execute("INSERT INTO monitoramento_registro (sala_acesso, usuario_id) VALUES (%s, %s)", (os.environ['SALA'], usuarioLogin.usuario_id,))
        except (Exception, psycopg2.Error) as error:        
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
            cursor.execute("SELECT * FROM AUTH_USER WHERE senha = '%s'", (usuarioConsulta.senha,))            
            
        except (Exception, psycopg2.Error) as error:
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
            #cursor.execute("SELECT * FROM AUTH_USER WHERE senha = '%s'", (senha,))   
            #Inner join criado para o postgres devido a sua limitação.
            cursor.execute("""SELECT b.* 
                            FROM AUTH_USER AS b 
                            INNER JOIN 
                                (
                                    SELECT "senhaPorta", usuario_id_id
                                    FROM users_acesso
                                    AS a
                                )AS a 
                            ON b.id=a.usuario_id_id
                            WHERE a."senhaPorta" = '%s'""", (senha,))           
            
        except (Exception, psycopg2.Error) as error:
            print("Falha ao obter o registro: {}".format(error))
        else:
            return cursor.fetchone()                                 
        finally:
            con.close()
            cursor.close()