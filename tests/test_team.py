import json


ENDPOINT = "/team"

#nenhum time foi cadastrado então não é para ter nenhum registro e essa validação é feita
def test_team_get_empty_teams(client):
    response = client.get(ENDPOINT)
    assert response.status_code == 200
    assert len(response.json) == 0

#usa-se diferentes payloads incorretos (com mais de seis pokemons, com zero etc...)
#O esperado e que todos deem erro com status code 400
#e que o corpo de retorno possua os campos do modelo padrão da mensagem de erro que é enviada ao usuário.
def test_team_save_team_with_error_payload(client, const):
    response = client.post(
        ENDPOINT, content_type=const.CONTENT_TYPE, data=json.dumps(const.TEAMS[6]))
    assert response.status_code == 400
    response_keys = response.json.keys()
    assert 'code' in response_keys
    assert 'name' in response_keys
    assert 'description' in response_keys
    response = client.post(
        ENDPOINT, content_type=const.CONTENT_TYPE, data=json.dumps(const.TEAMS[0]))
    assert response.status_code == 400
    response_keys = response.json.keys()
    assert 'code' in response_keys
    assert 'name' in response_keys
    assert 'description' in response_keys
    response = client.post(
        ENDPOINT, content_type=const.CONTENT_TYPE, data=json.dumps(const.TEAMS[9]))
    assert response.status_code == 400
    response_keys = response.json.keys()
    assert 'code' in response_keys
    assert 'name' in response_keys
    assert 'description' in response_keys
    response = client.post(
        ENDPOINT, content_type=const.CONTENT_TYPE, data=json.dumps(const.TEAMS[10]))
    assert response.status_code == 400
    response_keys = response.json.keys()
    assert 'code' in response_keys
    assert 'name' in response_keys
    assert 'description' in response_keys
    response = client.post(
        ENDPOINT, content_type=const.CONTENT_TYPE, data=json.dumps(const.TEAMS[11]))
    assert response.status_code == 400
    response_keys = response.json.keys()
    assert 'code' in response_keys
    assert 'name' in response_keys
    assert 'description' in response_keys    


#salva times com diferentes caracteristicas mas dentro do que é permitido
#é esperado que todas as requisições sejam processadas com sucesso.
def test_team_save_new_teams(client, const):
    response = client.post(
        ENDPOINT, content_type=const.CONTENT_TYPE, data=json.dumps(const.TEAMS[7]))
    assert response.status_code == 200
    assert response.json == const.SUCCESSFUL_MESSAGE
    response = client.get(ENDPOINT)
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['TRAINER'] == const.TEAMS[7]['trainer']
    assert response.json[0]['TEAM'] == const.TEAMS[7]['team']
    response = client.post(
        ENDPOINT, content_type=const.CONTENT_TYPE, data=json.dumps(const.TEAMS[8]))
    assert response.status_code == 200
    assert response.json == const.SUCCESSFUL_MESSAGE
    response = client.get(ENDPOINT)
    assert response.status_code == 200
    assert len(response.json) == 2
    assert response.json[1]['TRAINER'] == const.TEAMS[8]['trainer']
    assert response.json[1]['TEAM'] == const.TEAMS[8]['team']

#Tenta-se salvar um time já cadastrado no teste anterior novamente
#É esperado erro pois como já existe a operação tem de ser de edição não de criação.
def test_team_save_duplicate_team(client, const):
    response = client.post(
        ENDPOINT, content_type=const.CONTENT_TYPE, data=json.dumps(const.TEAMS[8]))
    assert response.status_code == 400
    response_keys = response.json.keys()
    assert 'code' in response_keys
    assert 'name' in response_keys
    assert 'description' in response_keys

#busca times com base no filtro de ID
#se houver cadastrado retorna, se não retorna um array vazio
def test_team_get_team_by_id(client, const):
    response = client.get(ENDPOINT+'/1')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['TRAINER'] == const.TEAMS[7]['trainer']
    response = client.get(ENDPOINT+'/2')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['TRAINER'] == const.TEAMS[8]['trainer']
    response = client.get(ENDPOINT+'/3')
    assert response.status_code == 200
    assert len(response.json) == 0

#busca todos os registros de times cadastrados previamente
def test_team_get_all_team(client):
    response = client.get('/team/')
    assert response.status_code == 200
    assert len(response.json) == 2

#busca os pokemons por time com base no id do time.
def test_team_get_team_pokemons(client, const):
    response = client.get(ENDPOINT+'/2/pokemons')
    print(response.json)
    assert response.status_code == 200
    assert len(response.json) == 6
    pokemons = const.TEAMS[8]['pokemons']

    for item in response.json:
        assert item['ID'] in pokemons

#testa a atualização do conjunto de pokemons de um time já existente
def test_team_update_team_pokemons(client, const):
    response = client.get(ENDPOINT+'/1/pokemons')
    assert response.status_code == 200
    old_pokemons = response.json[0]
    assert const.TEAMS[4]["pokemons"] != old_pokemons
    new_pokemons = const.TEAMS[4]["pokemons"]
    team = {
        "id": 1,
        "trainer": "Brock?",
        "team": "Update team",
        "pokemons": new_pokemons
    }
    response = client.put(
        ENDPOINT, content_type=const.CONTENT_TYPE, data=json.dumps(team))
    assert response.status_code == 200
    assert response.json == const.SUCCESSFUL_MESSAGE
    response = client.get(ENDPOINT+'/1/pokemons')
    assert response.status_code == 200
    assert len(response.json) == 4
    assert len(old_pokemons) > len(new_pokemons)

#cadastra e remove um time para verificar se o total de times aumentou e depois diminuiu.
def test_team_delete_team(client, const):
    response = client.get(ENDPOINT)
    assert response.status_code == 200
    assert len(response.json) == 2
    response = client.post(
        ENDPOINT, content_type=const.CONTENT_TYPE, data=json.dumps(const.TEAMS[1]))
    assert response.status_code == 200
    assert response.json == const.SUCCESSFUL_MESSAGE
    response = client.get(ENDPOINT)
    assert response.status_code == 200
    assert len(response.json) == 3
    response = client.delete(ENDPOINT+'/1')
    assert response.status_code == 200
    assert response.json == const.SUCCESSFUL_MESSAGE
    response = client.get(ENDPOINT)
    assert response.status_code == 200
    assert len(response.json) == 2

#remove todos os times existentes.
def test_team_remove_all_team(client, const):
    response = client.get(ENDPOINT)
    assert response.status_code == 200
    for item in response.json:
        response = client.delete(ENDPOINT+"/"+str(item['ID']))
        assert response.status_code == 200
        assert response.json == const.SUCCESSFUL_MESSAGE
    response = client.get(ENDPOINT)
    assert response.status_code == 200
    assert len(response.json) == 0
