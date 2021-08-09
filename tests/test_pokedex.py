
#testa o endpoint que recupera todos os pokemons
#valida o status code, se o primeiro registro é um dicionário e se ele é o primeiro pokemon
def test_pokedex_get_all_pokemons(client, const):
    response = client.get('/pokedex/')
    assert response.status_code == 200
    assert isinstance(response.json[0], dict)
    assert len(response.json) > 1
    assert response.json[0] == const.POKEMONS[0]

#testa o endpoint de busca de pokemon por nome
def test_pokedex_get_by_name(client, const):
    response = client.get('/pokedex/name/charizard')
    assert response.status_code == 200
    assert isinstance(response.json[0], dict)
    assert len(response.json) == 1
    assert response.json[0] == const.POKEMONS[2]

#testa o endpoint de busca de pokemon por numero (id)
def test_pokedex_get_by_number(client, const):
    response = client.get('/pokedex/number/4')
    assert response.status_code == 200
    assert isinstance(response.json[0], dict)
    assert len(response.json) == 1
    assert response.json[0] == const.POKEMONS[1]

#testa o endpoint de busca por tipos usando apenas um tipo
def test_pokedex_get_by_one_type(client, const):
    response = client.get('/pokedex/types/fire')
    assert response.status_code == 200
    assert isinstance(response.json[0], dict)
    assert len(response.json) > 1
    assert response.json[0] == const.POKEMONS[1]
    response = client.get('/pokedex/types/poison')
    assert response.status_code == 200
    assert isinstance(response.json[0], dict)
    assert len(response.json) > 1
    assert response.json[0] == const.POKEMONS[0]

#testa o endpoint de busca por tipos usando dois tipos
def test_pokedex_get_by_two_types(client, const):
    response = client.get('/pokedex/types/grass/poison')
    assert response.status_code == 200
    assert isinstance(response.json[0], dict)
    assert len(response.json) > 1
    assert response.json[0] == const.POKEMONS[0]
    response = client.get('/pokedex/types/flying/bug')
    assert response.status_code == 200
    assert isinstance(response.json[0], dict)
    assert len(response.json) > 1
    assert response.json[0] == const.POKEMONS[3]
