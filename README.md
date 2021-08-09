# Pokemon Méliuz #
## Observações ##
#### Sobre a implementação: ####
*   A ideia da construção desta API foi de ser a versão mais próxima possível para publicação em produção. Desta forma foi pensada em uma solução que inicialmente fosse usada para desenvolvimento e que para a publicação em produção necessitasse do menor número de ajustes possíveis. Por isso o docker foi usado, mas é perfeitamente possível usar sem.

*   Foi utilizado o servidor Http Simples, não foi usado o Gunicorn ou NGINX (apesar de serem os mais recomendáveis para o ambiente de produção) devido a falta de tempo hábil para implementação.

*   Foi usado o docker compose pois, apesar de haver apenas um container, já está estruturado para que caso precise, em um próximo momento outros containers serem iniciados junto com este.

*   Será observado que há um script no construtor da classe de persistência de dados, que verifica se existem todas as tabelas esperadas no banco de dados.  O motivo dessa escolha foi que por praticidade fora escolhido o SQLite para armazenar as informações, desta forma o script verifica a todo momento para certificar se a base de dados está disponível para o uso durante a demonstração. E tendo ciência de que este recurso deva ser desabilitado ao ir para produção e/ou caso se use outro SGBD.

*   A escolha em programar em Inglês foi apenas por gosto pessoal.


#### Sobre a stack utilizada: ####

*   Para programar a API foi escolhida a linguagem Python e o framework Flask por ter um pouco mais de familiaridade com esta linguagem para programação backend e que teria um menor tempo gasto de aprendizado dos recursos avançados da linguagem + framework, já o framework escolhido se deve ao fato de ser um micro framework e que atende aos requisitos da atividade proposta.

*   Para teste foi usado o Pytest por ser o padrão do mercado.

*   Para documentação foi usado o ApiDocJS por já ter trabalhado previamente com esta ferramenta.


## Arquivo Makefile ##

O projeto foi pensado para ser executado no Docker com os comandos no arquivo Makefile, para agilizar/automatizar os processos.

Os comandos disponíveis no Makefile são:

#### clean ####
Limpeza de arquivos temporários do python.

#### install: ####
Instala o `requirements.txt` via pip *(este comando é executado quando o build da imagem é feito)*.

#### test: ####
Prepara o ambiente para testes, inicia o container e executa os testes.

#### build: ####
Inicia o container dando build na imagem.    

#### venv: ####
Exporta as variáveis de ambiente para a sessão atual e para o arquivo .env que será lido quando iniciar a aplicação.

#### run: ####
Inicia o container sem dar build na imagem.

#### shell: ####
Alias para acessar o container.

#### stop: ####
Desliga o container

#### apidocjs ####
Reinicia o container, apaga a documentação antiga, cria a nova documentação e disponibiliza para visualização via navegador na porta
que está definida na variável de ambiente ```APIDOC_PORT``` que por padrão é ```49150```


## Instalação: ##

**:negative_squared_cross_mark: Localmente**

Caso for executar localmente sem o Docker, é necessário instalar ou já ter instalado: Python 3.6 e pip, e também Nodejs e NPM.

Após certificar-se de que possui as aplicações requeridas instaladas, acessar a raiz do projeto e executar os seguintes comandos:

*selecionando o ambiente virtual e instalando os pacotes necessários*

```
source venv/bin/activate
PYTHONPATH=venv
pip install -r requirements.txt
npm install apidoc -g
```

*criando o arquivo .env e setando as variáveis de ambiente.*
```
export FLASK_APP=pokemon_meliuz/app.py
export FLASK_ENV=development
export FLASK_HOST=0.0.0.0
export FLASK_PORT=5002
export PYTHONPATH=venv
export APIDOC_PORT=49150
echo "FLASK_APP=$(FLASK_APP)" > .env
echo "FLASK_ENV=$(FLASK_ENV)"  >> .env
echo "FLASK_HOST=$(FLASK_HOST)" >> .env
echo "FLASK_PORT=$(FLASK_PORT)" >> .env
echo "PYTHONPATH=$(PYTHONPATH)" >> .env
echo "APIDOC_PORT=$(APIDOC_PORT)" >> .env
```

*para iniciar a aplicação:*
Estará disponível em **http://localhost:5000/**
```
python ./pokemon_meliuz/app.py
```
### Para Executar os testes e atualizar a documentação: ###

*Executar os testes:*

```
rm -rf databases/test.db
FLASK_ENV=test pytest tests/ -v --cov=pokemon_meliuz

```
*Atualizar a documentação:*

```
sudo rm -rf ./docs/apidoc/
apidoc -i ./pokemon_meliuz/ -o ./docs/apidoc/

```

*Visualizar a documentação:*
Estará disponível em **http://localhost:49150/**
```
APIDOC_PORT=49150 #se já estiver em uso pode-se matar o processo ou trocar a porta
python ./docs/app.py

```

**:fish: Usando docker:**

*Criando o container:*
Em caso de build:
Estará disponível em **http://localhost/**
```
make build
```

*para iniciar a aplicação:*

Quando não precisar dar o build
Estará disponível em **http://localhost/**
```
make run
```

### Para Executar os testes e atualizar a documentação: ###

*Executar os testes:*

```
make test

```
*Atualizar e visualizar a documentação:*
Estará disponível em **http://localhost:49150/**
```
make apidocjs

```

*Para parar a aplicação:*

```
make stop

```
