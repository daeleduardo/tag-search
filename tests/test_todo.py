
def test_todo(client, const):
    response = client.get('/endpoint/')
    assert response.status_code == 200
    assert isinstance(response.json[0], dict)
    assert len(response.json) > 1
    assert response.json[0] == const.DATA_TODO