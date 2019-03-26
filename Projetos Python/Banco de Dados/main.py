from UsuarioDao import UsuarioDao
from Usuario import Usuario

#Instanciando o usuario
usuario1 = Usuario(15158, 'Teste', 'Autor Teste', 29)

#instanciando a classe UsuarioDao
usr = UsuarioDao()
usr.criarBanco()

result = usr.selecionarUsuario(usuario1.isbn)
if result[0] == 15158:
    print("sucesso: {}".format(result[0]))
else:
    print("falha: {}".format(result[0]))
