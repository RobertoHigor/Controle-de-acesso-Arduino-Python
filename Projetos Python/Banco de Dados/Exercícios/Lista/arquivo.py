import time
"""
    Tuples
"""
#Somar qualquer quantidade de valor vinda de uma Tuples
#*args é o sinal gather(*) dizendo que aceita qualquer quantidade de argumetnos
def sumall(*args):
    total = 0
    #a tupla em si é o primeiro argumento (no caso args[0])
    for valor in args[0]:
        total += valor
    #retorna uma tupla com a soma total e o maior número recebido
    return total, max(args[0])

"""
    Métodos de busca
"""
def checar_palavra(lista, palavra):
    for indice, valor in enumerate(lista):
        if palavra == valor:
            return True

#Buscar uma palavra no dicionário. Nesse caso está buscando a chave, pois o valor é aleatório
def checar_palavra_dicionario(dicionario, palavra):
    for chave in dicionario:
        if palavra == chave:           
            return True

#buscando se as letras alternativas da palavra (pulando 2 em 2) formam outras palavras que estejam na lista
def interlock(lista, palavra):
    par = palavra[::2]
    impar = palavra[1::2]
    return busca_binaria(lista, par) and busca_binaria(lista, impar)

#busca binária
def busca_binaria(lista, palavra):
    indice = len(lista) // 2

    if len(lista) == 0:
        return False

    if lista[indice] == palavra:        
        return True  

    if palavra > lista[indice]:  
        #Caso a palavra esteja depois da metade, retorna uma busca
        #Com um subconjunto maior que a metade (indice +1)   
        return busca_binaria(lista[indice+1:], palavra)
    else:
        #Caso esteja antes do meio, retorna um subconjunto 
        #apenas com os elementos antes do meio
        return busca_binaria(lista[:indice], palavra)
        
#Comando para pesquisar se possui alguma palavra igual ao inverso do argumento
def reverse_pair(lista, palavra):
    #Esse é um subconjunto que inverte uma lista/string
    reversa = palavra[::-1]
    return busca_binaria(lista, reversa)

"""
    Métodos de criar lista ou dicionário através de um arquivo de texto
"""

def make_word_list_append():
    #Ler linhas de um arquivo e construir uma lista utilizando make_word_list_append
    t = []
    fin = open('C:\\Users\\higor\Desktop\Arquivos Importantes\\Faculdade\\Desenvolvimento\\Python\\tcc-roberto\\Projetos Python\\Banco de Dados\\Exercícios\\Lista\\words.txt')
    for line in fin:
        word = line.strip()
        t.append(word)
    return t

def make_word_list_dictionary():
    dicionario = dict()
    fin = open('C:\\Users\\higor\Desktop\Arquivos Importantes\\Faculdade\\Desenvolvimento\\Python\\tcc-roberto\\Projetos Python\\Banco de Dados\\Exercícios\\Lista\\words.txt')
    i = 0
    for line in fin:
        word = line.strip()
        dicionario[word] = i + 1
    return dicionario

def make_word_list_assign():
    #Ler linhas de um arquivo e construir uma lista utilizando make_word_list_append
    t = []
    fin = open('C:\\Users\\higor\Desktop\Arquivos Importantes\\Faculdade\\Desenvolvimento\\Python\\tcc-roberto\\Projetos Python\\Banco de Dados\\Exercícios\\Lista\\words.txt')
    for line in fin:
        word = line.strip()
        #Só pode concatenar um elemento de lista, não uma "str"
        #Nesse caso utiliza [word] entre colchetes
        t += [word]    
    return t

"""
    Método main
"""
#Criando a lista T e contando o tempo
start_time = time.time()
t = []
t = make_word_list_append()
t.sort()
elapsed_time = time.time() - start_time
#print(t)
#print(elapsed_time, 'seconds')

#Criando a lista t2 e contando o tempo
start_time = time.time()
t2 = []
t2 = make_word_list_assign()
#finalizando o tempo
elapsed_time = time.time() - start_time
#print(t2)
#print(elapsed_time, 'seconds')

"""
    Buscando palavras
"""

#busca linear
start_time = time.time()
checar_palavra(t, 'vida')
elapsed_time = time.time() - start_time
print(elapsed_time, 'seconds busca linear')

#busca binária
start_time = time.time()
busca_binaria(t, 'vida')
elapsed_time = time.time() - start_time
print(elapsed_time, 'seconds busca binaria')

#buscando reverse pair (uma palavra que é o inverso da outra)
for palavra in t:
    if reverse_pair(t, palavra):
       print(palavra)

#imprimindo palavra "interlock" (onde letras alternativas formam uma palavra)
for palavra in t:
    if interlock(t, palavra):
        print(palavra[::2], palavra[1::2], palavra)

"""
    Dicionário 
"""

dicionario = dict()
dicionario = make_word_list_dictionary()
#print(dicionario)

if checar_palavra_dicionario(dicionario, "arroz"):
    print(dicionario["arroz"])

"""
    Tuples
"""
t = (2, 5, 7, 10)
print(sumall(t))