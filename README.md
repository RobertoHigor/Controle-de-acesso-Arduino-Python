# TCC-Roberto

Programa desenvolvido em python que se comunica com um servidor arduino. O arduino envia uma senha para o programa poder validar se existe um usu�rio com essa senha. Caso exista, ele envia um sinal para que o arduino libere a porta e registra esse acesso na tabela de registros.

# Arduino

O programa ir� esperar o input no teclado num�rico at� que o usu�rio aperte a tecla "*". Ap�s recebido, ele envia para o python atrav�s da porta serial.

# Pr�-requisitos Python
pip install pyserial

# Pr�-requisitos Arduino
Keypad.h

