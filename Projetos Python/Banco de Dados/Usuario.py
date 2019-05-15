import UsuarioDao
class Usuario:
    def __init__(self, usuario_id, senha, usuario, primeiroNome, ultimoNome, email):
        self.usuario_id = usuario_id
        self.senha = senha
        self.usuario = usuario       
        self.primeiroNome = primeiroNome
        self.ultimoNome = ultimoNome      
        self.email = email

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


     
