import os

#verifica se o nome da aplicação é o que foi configurado previamente
def test_app_name(app):
    assert app.name == "pokemon_meliuz.app"

#verifica se a mudança do ambiente para teste ocorreu com sucesso.
def test_app_env():
    assert os.getenv('FLASK_ENV') == 'test'

#verifica se aplicação está rodando
def test_app_request_200(client):
    assert client.get('/').status_code == 200

#tenta acessar um endpoind não existente e deve retornar erro 404
def test_app_request_404(client):
    assert client.get('/url/not/found').status_code == 404

#verifica se a aplicação recebeu a primeira requisição
def test_app_receive_request(app):
    assert app.got_first_request == True
