import time
import math

def print_n(s, n):
    if n<=0:
        return
    print(s)
    print_n(s, n-1)

def nested_sum(testes):
    soma = 0
    for x in range(len(testes)):              
        for teste in range(len(testes[x])):
            soma += t[x][teste]
    return soma

    """
        alternativa
    for nested in t:
        soma += sum(nested)
    return soma
    """
def cumsum(testes):   
    lista = []
    soma = 0
    for teste in range(len(testes)):        
        lista.append(testes[teste] + soma) 
        soma += testes[teste]  
    return lista

def middle(testes):   
    #pois a lista também é contada do negativo pra baixo (começando do final)
    return testes[1:-1]

#igual o middle porém não retorna nada
def chop(testes):
    del testes[0]
    del testes[-1]

#Esperado imprimir a soma (21)
t = [[1,2], [3], [4, 5, 6]]
print(nested_sum(t))

#esperado imprimir o numero + seus anteriores (1, 3, 6)
t2 = [1, 2, 3]
print(cumsum(t2))

#Esperado imprimir apenas o 2 e o 3
t3 = [1, 2, 3, 4]
t3 = middle(t3)
print(t3)

#modificar a lista sem retorno
t4 = [1, 2, 3, 4]
chop(t4)
print(t4)