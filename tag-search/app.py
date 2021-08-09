import os
from flask import Flask, render_template, jsonify, json, request, Response,g
from dotenv import load_dotenv
from flask_caching import Cache
from werkzeug.exceptions import HTTPException
from .ext import models , middleware
from .blueprints.contact import views

#metodo que cria/inicia a aplicação
def create_app():

    app = Flask(__name__)
    #adiciona o cache
    app.config['CACHE_TYPE'] = 'simple'
    app.cache = Cache(app)
    #carrega os metadados do banco de dados
    models.base.metadata.create_all(models.engine)
    #carrega as variaveis de ambiente
    load_dotenv()
    #adiciona as rotas da aplicação 
    add_routes(app)
    #adiciona na aplicação o método responsável tratar a mensagem de erro e retornar ao usuário
    add_error_handler(app)
    return app

#método que recebe as mensagens e retorna em um formato padrão para o usuário.
#Por padrão em todos os erros, seja por Except ou por lançamento de erro quando não passa em uma validação,
#E feito no seguinte padrão: TipoErro('Mensagem',número)
#exemplo: raise DataError("Can't handle team information, please check your payload", 400)

def add_error_handler(app):
    @app.errorhandler(Exception)
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = None
        if isinstance(e, HTTPException):
            response = e.get_response()
            response.data = json.dumps({
                "code": e.code,
                "name": e.name,
                "description": e.description,
            })
        else:
            response = Response(status=e.args[1])
            response.data = json.dumps({
                "code": e.args[1],
                "name": "Error to process request",
                "description": e.args[0],
            })
        response.content_type = "application/json"
        return response

#Adiciona as rotas e blueprints
def add_routes(app):
    @app.route('/')
    @middleware.jwt_verify
    def index():
        return render_template("admin.html")    
    app.register_blueprint(views.contact)

if __name__ == '__main__':
    create_app().run(host=os.getenv('FLASK_HOST'), port=os.getenv('FLASK_PORT'))
    



