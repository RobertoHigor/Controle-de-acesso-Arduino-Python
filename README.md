# TCC-Roberto

Programa desenvolvido em python que se comunica com um servidor arduino. O arduino envia uma senha para o programa poder validar se existe um usuário com essa senha. Caso exista, ele envia um sinal para que o arduino libere a porta e registra esse acesso na tabela de registros.

# Arduino

O programa irá esperar o input no teclado numérico até que o usuário aperte a tecla "*". Após recebido, ele envia para o python através da porta serial.

# Pré-requisitos Python
pip install pyserial

# Pré-requisitos Arduino
Keypad.h

