# TCC-Roberto

Programa desenvolvido em python que se comunica com um servidor arduino. O arduino envia uma senha para o programa poder validar se existe um usuário com essa senha. Caso exista, ele envia um sinal para que o arduino libere a porta e registra esse acesso na tabela de registros.

### Instalação

## Aplicação Python

# Criando ambiente virtual
É necessário instalar o pacote virtualenv para que seja possível criar um ambiente virtual onde será instalado as bibliotecas sem que haja conflito com as já existentes no computador.

Para se instalar o virtualenv baixa digitar o comando `pip install virtualenv`

Após instalado, ele irá criar um arquivo chamado virtualenv.exe na pasta Scripts/ dentro da pasta onde está instalado o Python, no meu caso por utilizar o Python 3.7 32bits está na pasta Python37-32/

Para criar o ambiente virtual, deve-se executar o arquivo virtualenv.exe seguido da pasta onde será armazenado o ambiente virtual (no meu caso foi utilizado uma pasta chamada env dentro da pasta raíz do projeto)

O comando ficou `virtualenv.exe env --no-site-packages` pelo fato do arquivo virtualenv.exe já estar nas variáveis do sistema. O argumento --no-site-packages possibilita uma instalação limpa, sem adicionar os pacotes já já estão instalados no sistema.

Após instalado, deve-se entrar dentro do ambiente virtual criado executando o arquivo activate dentro da pasta Scripts criadas, nesse caso o comando é `env\Scripts\Activate`. Sempre que for executar o programa, é necessário ativar o ambiente virtual. Para sair do ambiente virtual basta utilizar o comando deactivate.

# Pré-requisitos Python
A lista de pré-requisitos se encontra no arquivo requirements.txt sendo os principais a biblioteca pySerial (3.4)para realizar a comunicação com o arduino e a psycopg2 (2.8.2) para o banco de dados PostgresSQL

```
pip install pyserial
pip install psycopg2
```

Para se instalar as bibliotecas que foram utilizadas, basta executar o seguinte comando dentro do ambiente virtual
`pip install -r requirements.txt`

# Instruções para execução
É necessário entrar no ambiente virtual. Após isso, é preciso alterar a porta no qual o Arduino está conectado na variável arduino no arquivo main.py. Por padrão está a porta COM4.
Com o banco de dados sendo executado junto do arduino, basta executar o código através do comando `python main.py` que ele já vai estar funcionando em loop esperando uma mensagem do Arduino.

obs: Alterar a coluna data_acesso para o valor default now()

## Arduino
O programa irá esperar o input no teclado numérico até que o usuário aperte a tecla "*". Após recebido, ele envia para o python através da porta serial.

É necessário a instalação da [Arduino IDE](https://www.arduino.cc/en/Main/Software) que já inclui os drivers necessários para o Arduino. Em seguida é preciso que seja criado um projeto na IDE para que seja possível o envio do código para a placa Arduino.

# Pré-requisitos Arduino
Keypad.h

A biblioteca já se encontra no Arduino IDE, sendo apenas necessário ir em Sketch>Incluir Biblioteca>Keypad. Caso não encontre a biblioteca, pode ser necessário que busque em Sketch>Incluir Biblioteca>Gerenciar bibliotecas.

# Instalação
Crie um projeto com o código do arquivo arduinoBanco.ino e em seguida importe as bibliotecas necessárias. Após isso só preciso clicar e enviar e verificar se o envio foi feito com sucesso. O Arduino já estará executando o código aguardando a conexão e execução da aplicação em Python.

## Banco de dados PostgresSQL

O banco de dados é onde será armazenado as senhas dos usuários além dos registros de entrada. A criação do banco de dados será feita pelo Django utilizando a ORM porém é necessário que seja instalado o PostgresSQL para que seja executado o banco de dados.
A versão utilizada foi a 11.3-1

# Como executar
Basta inicializar o serviço no caso do windows, pode ser feito apertando windows + r e digitando services.msc para localizar e inicalizar o serviço postgresql-x64-11.
O PostgresSQL provém uma interface gráfica pelo aplicativo pgAdmin4.
