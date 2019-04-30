import UsuarioDao
class Usuario:
    def __init__(self, nome, usuario, senha):
        self.nome = nome
        self.usuario = usuario
        self.senha = senha

    """#Declarando as variáveis do Livro
    def __init__(self, isbn, titulo, autor, preco):
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.preco = preco"""

#EM python não se usa getters e setters, então caso queira fazer algo deve-se usar de propriedades
"""
    #equivalente a getter
    @property
    def titulo(self):
        #faça alguma coisa
        return self.titulo
    
    #equivalente a setter
    def titulo(self, valor):
        self.titulo = valor
"""


     
