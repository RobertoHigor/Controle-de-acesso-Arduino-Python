from ConnectionFactory import ConnectionFactory
import psycopg2
from psycopg2 import Error
from Usuario import Usuario
#exceptions https://codereview.stackexchange.com/questions/187951/crud-operations-for-a-contact-list-using-pymysql

#Classe responsável pelos querys no banco de dados
class UsuarioDao:  
    # Lista de salas
    # l = Laboratório de robótica
    # d = Sala da diretora
    # m = Manuntenção
    # As salas com números serão as salas numeradas	
    salasDicionario = {'l':['Laboratório', 3], 'd':['Direção', 2], 'm':'Manutenção', 1:'1 Periodo', 2:'2 Periodo', 3:'3 Periodo', 4:'4 Periodo', 5:'5 Periodo'}
    def inserirUsuario(self, novoUsuario):
        try:
            con = ConnectionFactory.conectar()
            cursor = con.cursor()                    
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
        try:
            con = ConnectionFactory.conectar()
            cursor = con.cursor()       
            cursor.execute("INSERT INTO monitoramento_registro (sala_acesso, usuario_id) VALUES ('{0}', '{1}')".format(self.salasDicionario[sala][0], usuarioLogin.usuario_id))
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
            cursor.execute("SELECT * FROM AUTH_USER WHERE senha = '{0}'".format(usuarioConsulta.senha))            
            
        except (Exception, psycopg2.Error) as error:
            print("Falha ao obter o registro: {}".format(error))
        else:
            #return cursor.fetchall()
            return cursor.fetchone()
        finally:
            con.close()
            cursor.close()

    def checarPermissaoUsuario(self, usuario_id, sala):      
        try:
            con = ConnectionFactory.conectar()
            cursor = con.cursor()          
                        
            cursor.execute("""SELECT user_id, group_id 
                            FROM auth_user_groups
                            WHERE user_id = '{0}' AND group_id = '{1}' """.format(usuario_id, self.salasDicionario[sala][1]))

            usuarioComPermissao = cursor.fetchone()                
            
        except (Exception, psycopg2.Error) as error:
            print("Falha no checarPermissaoUsuario: {0}".format(error))
        else:
            if (usuarioComPermissao): return True
            else: return False                              
        finally:
            con.close()
            cursor.close()

    def logarUsuario(self, senha, sala):
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
                            WHERE a."senhaPorta" = '{0}'""".format(senha)) 
            usuario = cursor.fetchone()
            
            usuarioTemPermissao = self.checarPermissaoUsuario(usuario[0], sala)
            
        except (Exception, psycopg2.Error) as error:
            print("Falha ao obter o registro em logarUsuario(): {0}".format(error))
        else:
            if (usuarioTemPermissao): return usuario   
            else: return None                           
        finally:
            con.close()
            cursor.close()
