from ConnectionFactory import ConnectionFactory
import psycopg2
from psycopg2 import Error
from Usuario import Usuario
#exceptions https://codereview.stackexchange.com/questions/187951/crud-operations-for-a-contact-list-using-pymysql

#Classe responsável pelos querys no banco de dados
class UsuarioDao:  

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

    def inserirLog(self, usuarioLogin, sala):
        # Lista de salas
        # l = Laboratório de robótica
        # d = Sala da diretora
        # m = Manuntenção
        # As salas com números serão as salas numeradas		
        if sala == "l":
            sala = "Laboratório"
        elif sala == "d":
            sala = "Direção"
        elif sala == "m":
            sala = "Manutenção"
        elif sala == "1":
            sala = "Sala 1"
        elif sala == "2":
            sala = "Sala 2"
		elif sala == "3":
			sala = "Sala 3
        elif sala == "4":
            sala = "Sala 4"
        elif sala == "5":
            sala = "Sala 5"
        elif sala = "6"
            sala = "Sala 6"

		

        try:
            con = ConnectionFactory.conectar()
            cursor = con.cursor()            
            cursor.execute("INSERT INTO monitoramento_registro (sala_acesso, usuario_id) VALUES (%s, %s)", (sala, usuarioLogin.usuario_id,))
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
