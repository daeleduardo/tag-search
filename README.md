# TAG SEARCH #

## Objetivo ##

Criar um sistema de busca de atividades e locais, na forma de um buscador, onde se previamente cadastra as atividades e locais, e a partir de uma busca, o usuário poderá encontrar os locais e atividades que ele/ela deseja.


## Endereços ##

Para acessar o sistema, basta acessar o endereço para o qual a aplicação publicada.
Para acessar o modo administrador, acessar o endereço:`[endereço da aplicacao]/admin`

## Configurações ##

Antes de publicar, é necessário configurar o sistema. Para isto siga os seguintes passos:

1 . Criar o arquivo ENV:
Copiar o arquivo .env.example para .env e alterar os valores de acordo com o seu ambiente.

2 . Gerar chaves RS256
Gerar as chaves RS256 para uso no token JWT e salva-las na raiz do projeto.

## Execução ##

No atual momento, o sistema está em desenvolvimento, no entanto é possível executar o sistema em modo de teste, para isso basta executar os comandos dentro da pasta raiz do projeto:

``source venv/bin/activate``
``pip3 install -r requirements.txt``
``export FLASK_APP=tag-search/app.py``
``flask run``


## Débitos Técnicos ##

*   Terminar as configurações para rodar em docker.
*   Terminar as automações do arquivo Makefile.
*   Implementar os testes.
*   Criar uma tela de gestão de usuários
*   Implementar o sistema de recuperação de senha
*   Criar automação de publicação com minificação dos arquivos de javascropt e css.




