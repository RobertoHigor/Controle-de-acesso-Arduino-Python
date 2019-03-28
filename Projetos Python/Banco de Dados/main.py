from UsuarioDao import UsuarioDao
from Usuario import Usuario

#Instanciando as classes
usuario1 = Usuario('Zuko Iroh', 'zukofire', 15158)
usr = UsuarioDao()

#Criar o banco de dados e inserir usuário
#usr.criarBanco()
#usr.inserirUsuario(usuario1)

result = usr.selecionarUsuario(usuario1)
if result[0] == 15158:
    print("sucesso: {}".format(result[0]))
else:
    print("falha: {}".format(result[0]))
