import json
import types

from flask import Flask
from flask.testing import FlaskClient

from routes.api.vending_machine_routes import vending_machine_controller


def setup_module(module: types.ModuleType) -> None:
    app = Flask(__name__)
    app.register_blueprint(vending_machine_controller)
    app.config["TESTING"] = True


def test_create_vending_machine_api(client: FlaskClient) -> None:
    # Test successful vending machine creation
    data = {"name": "ven1", "location": "A"}
    response = client.post(
        "/machine/create-machine",
        data=json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == 200
    # assert json.loads(response.data) == {'success': True, 'message': 'Test vending machine information'}

    # # Test vending machine creation with existing name
    # data = {"name": "Test Vending Machine", "location": "Test Location"}
    # response = client.post("/machine/create-machine", data=json.dumps(data), content_type='application/json')
    # assert response.status_code == 400
    # assert json.loads(response.data) == {'success': False,
    #                                      'message': "Vending machine with name 'Test Vending Machine' already exists."}
    #
    # # Test vending machine creation with missing required parameters
    # data = {"location": "Test Location"}
    # response = client.post("/machine/create-machine", data=json.dumps(data), content_type='application/json')
    # assert response.status_code == 500
    # assert json.loads(response.data) == {'success': False,
    #                                      'message': 'An error occurred while creating the vending machine'}
