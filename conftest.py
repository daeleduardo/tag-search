#arquivo executado antes de iniciar os testes
import pytest
from tag-search.app import create_app
#classe com os dados que serão usados para validar as requisições
class constants():
    CONTENT_TYPE = "application/json"

    DATA_TEST = {}

    SUCCESSFUL_MESSAGE = {"success": True}

#cria a fixture de app para usar como injeção de dependência nos próximos testes.
@pytest.fixture(scope="module")
def app():
    """Instance of Main flask app"""
    return create_app()
#cria a fixture da classe de constantes para usar como injeção de dependência nos próximos testes.
@pytest.fixture(scope="module")
def const():
    return constants()
