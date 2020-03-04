from ConnectionFactory import ConnectionFactory
import psycopg2
from psycopg2 import Error
from Usuario import Usuario
#exceptions https://codereview.stackexchange.com/questions/187951/crud-operations-for-a-contact-list-using-pymysql

#Classe responsável pelos querys no banco de dados
class UsuarioDao:  
    # Lista de salas.
    #Cada caractere único é associado a uma sala, contendo seu nome e ID do grupo no banco de dados    
    salasDicionario = {'d':['Direção', 2],     
     'l':['Laboratório', 3],
     'm':['Manutenção', 4],
      1:['1 Periodo', 5],
      2:['2 Periodo', 6],
      3:['3 Periodo', 7],
      4:['4 Periodo', 8],
      5:['5 Periodo', 9]}

    #Inseri o registro do acesso feito com sucesso
    def inserirRegistroDeAcesso(self, usuario, sala):
        try:
            con = ConnectionFactory.conectar()
            cursor = con.cursor()       
            cursor.execute("INSERT INTO monitoramento_registro (sala_acesso, usuario_id) VALUES ('{0}', '{1}')".format(self.salasDicionario[sala][0], usuario[0]))
        except (Exception, psycopg2.Error) as error:        
            print("Falha ao inserir o registro: {}".format(error))
        else:
            con.commit()
        finally:
            con.close()
            cursor.close()

    #Checa se o usuário possui permissão na sala que deseja acessar
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

    #Checa se o usuário existe no banco de dados
    def usuarioExiste(self, senha, sala):
        try:
            con = ConnectionFactory.conectar()
            cursor = con.cursor()           
            #Inner join criado para o postgres devido a sua limitação de query.
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
            if (usuarioTemPermissao):     
                self.inserirRegistroDeAcesso(usuario, sala)
                return True 
            else: return False                           
        finally:
            con.close()
            cursor.close()
