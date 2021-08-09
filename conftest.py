#arquivo executado antes de iniciar os testes
import pytest
from pokemon_meliuz.app import create_app
#classe com os dados que serão usados para validar as requisições
class constants():
    CONTENT_TYPE = "application/json"

    POKEMONS = [ 
                    {
                        "HEIGHT": 0.7,
                        "ID": 1,
                        "IMAGE": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png",
                        "NAME": "bulbasaur",
                        "TYPES": [
                        "poison",
                        "grass"
                        ],
                        "WEIGHT": 6.9,
                        "XP": 64
                    },

                    {
                        "HEIGHT": 0.6,
                        "ID": 4,
                        "IMAGE": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png",
                        "NAME": "charmander",
                        "TYPES": [
                        "fire"
                        ],
                        "WEIGHT": 8.5,
                        "XP": 62
                    },

                    {
                        "HEIGHT": 1.7,
                        "ID": 6,
                        "IMAGE": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/6.png",
                        "NAME": "charizard",
                        "TYPES": [
                        "fire",
                        "flying"
                        ],
                        "WEIGHT": 90.5,
                        "XP": 240
                    },

                    {
                        "HEIGHT": 1.1,
                        "ID": 12,
                        "IMAGE": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/12.png",
                        "NAME": "butterfree",
                        "TYPES": [
                        "flying",
                        "bug"
                        ],
                        "WEIGHT": 32.0,
                        "XP": 178
                    }
                ]

    TEAMS = [
            {
                "team": "Team 0",
                "trainer": "Trainer 0",
                "pokemons": []
            },
            {
                "team": "Team 1",
                "trainer": "Trainer 1",
                "pokemons": [133]
            },
            {
                "team": "Team 2",
                "trainer": "Trainer 2",
                "pokemons": [33,30]
            },
            {
                "team": "Team 3",
                "trainer": "Trainer 3",
                "pokemons": [147,148,149]
            },
            {
                "team": "Team 4",
                "trainer": "Trainer 4",
                "pokemons": [39,40,36,35]
            },
            {
                "team": "Team 5",
                "trainer": "Trainer 5",
                "pokemons": [150,151,144,145,146]
            },        
            {
                "team": "Ash",
                "trainer": "Ash",
                "pokemons": [25,1,7,6,18,12]
            },
            {
                "team": "Aqua Team",
                "trainer": "Misty",
                "pokemons": [120,54,118,121,116,175]
            },
            {
                "team": "Pallet Team",
                "trainer": "Ash Ketchum",
                "pokemons": [25,1,7,6,18,12]
            },
            {
                "team": 0,
                "trainer": 0,
                "pokemons": [11,14,129]
            },
            {
                "team": "Brock",
                "trainer": "",
                "pokemons": [41,95,74,113,37,128,124]
            },
            {
                "trainer": "Failure",
                "pokemons": [120,54,118,121,116,175]
            },              
        ]

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
