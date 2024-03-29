
from importlib.machinery import SourceFileLoader
from fastapi.testclient import TestClient
from pathlib import Path
_me_parent = Path(__file__).absolute().parent
_one_level_up = _me_parent.parent
fapi_server_path = f'{_one_level_up}/fapi_server.py'
app = SourceFileLoader('fapi_server', fapi_server_path).load_module().app


def test_read_root():
    # arrange
    client = TestClient(app)

    # act
    response = client.get("/")
    data = response.json()

    # assert
    assert response.status_code == 200
    assert data["msg"] == {"Hello": "World"}


def test_load_db():
    # arrange
    client = TestClient(app)

    # act
    response = client.get("/load_db/2466_tokens.txt")
    data = response.json()

    # assert
    assert response.status_code == 200
    assert data["len"] == 26


def test_add_to_db():
    # arrange
    client = TestClient(app)
    token1 = "tok_tester"
    token2 = "tok_tester_2"
    token3 = "game_changer"

    # test for adding 1 token
    # act
    response = client.get("/add_to_db/" + token1)
    data = response.json()
 
    # assert
    assert response.status_code == 200
    assert data["token"] == token1
    assert data["len"] >= 1

    response = client.get("/get_suggestions/" + token1)
    data = response.json()
    assert token1 in data["result"]
    

def test_get_suggestions():
    # arrange
    client = TestClient(app)
    client.get("/load_db/2466_tokens.txt")
    prefix = "sympt"
    
    # act
    response = client.get("/get_suggestions/" + prefix)
    data = response.json()

    # assert
    assert response.status_code == 200
    assert data["prefix"] == prefix
    assert data["limit"] == 10
    assert data["result"] == ['symptomatic']
