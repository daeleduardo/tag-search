# -*- coding: utf-8 -*-
import os, sys
from unicodedata import category


sys.path.append(os.getcwd())
sys.path.append(os.getcwd()+"/tag_search")
sys.path.append(os.getcwd()+"/tag_search/ext")

from flask import Flask, render_template, json, Response, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
from sqlalchemy import inspect
from sqlalchemy.exc import DataError, DatabaseError
from werkzeug.exceptions import HTTPException
from ext import models, cache as cachemodule, utils, constants
from blueprints.place import views as viewsPlace
from blueprints.user import views as viewsUser



csrf = CSRFProtect()
cache = cachemodule.cache

def create_app():

    app = Flask(__name__)
    # carrega as variaveis de ambiente
    load_dotenv()
    load_appconfig(app)
    # adiciona as rotas da aplicação
    add_routes(app)
    # adiciona na aplicação o método responsável tratar a mensagem de erro e retornar ao usuário
    add_error_handler(app)
    check_if_first_run()
    return app

# método que recebe as mensagens e retorna em um formato padrão para o usuário.
# Por padrão em todos os erros, seja por Except ou por lançamento de erro quando não passa em uma validação,
# E feito no seguinte padrão: TipoErro('Mensagem',número)
# exemplo: raise DataError("Can't handle team information, please check your payload", 400)


def add_error_handler(app):
    @app.errorhandler(404)
    def page_not_found(e):
        # note that we set the 404 status explicitly
        return render_template('404.html'), 404

    @app.errorhandler(Exception)
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = None

        if is_treated_error(e):

            response = e.get_response()
            response.data = json.dumps({
                "code": e.code,
                "name": e.name,
                "description": e.description,
            })
        else:
            status_code_error = 500 if len(e.args) == 1 else e.args[1]
            msg_code_error = e.args[0] if len(e.args) > 0 else ''
            response = Response(status=status_code_error)
            response.data = json.dumps({
                "code": status_code_error,
                "name": "Error to process request",
                "description": msg_code_error,
            })
        response.content_type = "application/json"
        return response

# Adiciona as rotas e blueprints


def add_routes(app):
    @csrf.exempt
    @app.route('/')
    @cache.cached(timeout=constants.cache_time.END_CURRENT_DAY, query_string=True)
    def index():
        return render_template("index.html")

    @app.route('/admin')
    @cache.cached(timeout=constants.cache_time.END_CURRENT_DAY, query_string=True)
    def admin():
        return redirect(url_for('user.admin'))
    app.register_blueprint(viewsPlace.place)
    app.register_blueprint(viewsUser.user)



def load_appconfig(app):
    # adiciona o cache
    cache.init_app(app)
    # adiciona proteção CSRF
    csrf.init_app(app)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_TOKEN'] = os.getenv('JWT_TOKEN')
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_SECRET_KEY'] = os.getenv('WTF_CSRF_SECRET_KEY')
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['REMEMBER_COOKIE_SECURE'] = True
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_PRIVATE_KEY')
    app.config['JWT_PUBLIC_KEY'] = os.getenv('JWT_PUBLIC_KEY')

    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL')
    app.config['MAIL_DEBUG'] = os.getenv('MAIL_DEBUG')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    

def check_if_first_run():
    inspector = inspect(models.engine)
    tables = inspector.get_table_names()
    if len(tables) == 0:
        # carrega os metadados do banco de dados
        models.base.metadata.create_all(models.engine)

    # cria o usuário admin
    session = models.Session()
    exists_users = session.query(models.Users).first()
    if exists_users is None and os.getenv("ADMIN_DEFAULT_PASS") is not None:
        pwd = utils.utils.get_hash(os.getenv("ADMIN_DEFAULT_PASS"), only_numeric=False)
        first_user = models.Users(
            name="admin", email="admin@admin.com", password=pwd, 
            is_admin=True, is_active=True,id_create = 0)
        session.add(first_user)
        session.commit()

        #se é um ambiente de demonstração cria um local padrão
        if os.getenv("FLASK_ENV") == constants.env.MEMORY :
            place = models.Places(
                name = "Lagoa da Pampulha",
                category = "outros",
                latitude = "-19.852514986654832",
                longitude = "-43.97841670946394"
            )
            session.add(place)
            tags = ["lagoa", "pampulha"]
            for idx, tag in enumerate(tags):
                t = models.Tags(
                    name = tag,
                    hash_name = utils.utils.get_hash(tag)
                )
                pt = models.Placestags(
                    id_place = 1,
                    id_tag = (idx+1)
                )
                session.add(t)
                session.add(pt)
            session.commit()

def is_treated_error(e):
    is_treated_error = True
    is_treated_error = is_treated_error and isinstance(e, HTTPException)
    is_treated_error = is_treated_error and isinstance(e, DataError)
    is_treated_error = is_treated_error and isinstance(e, DatabaseError)
    is_treated_error = is_treated_error and isinstance(e, AttributeError)
    is_treated_error = is_treated_error and isinstance(e, TypeError)
    return  is_treated_error

if __name__ == '__main__':
    create_app().run(host=os.getenv('FLASK_HOST'), port=os.getenv('FLASK_PORT'))
