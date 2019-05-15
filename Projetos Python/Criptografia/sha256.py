import hashlib

str = "Teste"

result = hashlib.sha256(str.encode())

print("O hexadecimal é: ")

print(result.hexdigest())