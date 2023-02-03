import json

from flask import Response
from flask.testing import FlaskClient

from app import app


def client_post(client: FlaskClient, route: str, data: dict) -> Response:
    response = client.post(
        route, data=json.dumps(data), content_type="application/json"
    )
    return response


def client_get(client: FlaskClient, route: str) -> Response:
    response = client.get(route)
    return response


def test_purge_database_api() -> None:
    with app.test_client() as client:
        response = client.get("/api/purge-database")
        assert response.status_code == 200


def test_create_vending_machine_api() -> None:
    route = "/api/machine/create-machine"
    with app.test_client() as client:
        data = {"name": "ven1", "location": "A"}
        response = client_post(client, route, data)
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "success": True,
            "message": {"name": "ven1", "location": "A", "items": {}},
        }

        # Test vending machine creation with existing name
        data = {"name": "ven1", "location": "B"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Vending machine with name 'ven1' already exists.",
        }

        # Test vending machine creation with missing required argument
        data = {"location": "A"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Both 'name' and 'location' must be present in the request data",
        }

        # Test vending machine creation with excessive required argument
        data = {"name": "ven1", "location": "A", "items": "test"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Too many keys in the request data, require only 'name' and 'location'",
        }


def test_get_vending_machine_info_api() -> None:
    route = "/api/machine/get-machine"
    with app.test_client() as client:
        data = {"name": "ven1"}
        response = client_post(client, route, data)
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "success": True,
            "message": {"name": "ven1", "location": "A", "items": {}},
        }

        # Test get vending machine with non-exist name
        data = {"name": "non-exist"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Vending machine with name 'non-exist' does not exists.",
        }

        # Test get vending machine with no 'name' argument
        data = {"location": "A"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Missing 'name' in the request data",
        }

        # Test get vending machine with excessive required argument
        data = {"name": "ven1", "location": "A"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Too many keys in the request data, require only 'name'",
        }


def test_get_all_vending_machine_info_api() -> None:
    route = "/api/machine/get-all-machine"
    with app.test_client() as client:
        response = client_get(client, route)
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "success": True,
            "message": [{"name": "ven1", "location": "A", "items": {}}],
        }


def test_change_vending_machine_name_api() -> None:
    route = "/api/machine/change-name"
    with app.test_client() as client:
        data = {"name": ["ven1", "ven2"]}
        response = client_post(client, route, data)
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "success": True,
            "message": {"name": "ven2", "location": "A", "items": {}},
        }

        # Test change vending machine name with not exist vending machine name
        data = {"name": ["testtest", "ven2"]}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Vending machine with name 'testtest' does not exists.",
        }

        # Test change vending machine name with same value of old_name and new_name
        data = {"name": ["ven2", "ven2"]}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Old vending machine name: 'ven2' and new vending machine name: 'ven2' are the same",
        }

        # Test change vending machine name with missing name argument.
        data = {"location": "test"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Missing 'name' in the request data",
        }

        # Test change vending machine name with excessive argument.
        data = {"name": ["ven1", "ven2"], "location": "test"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Too many keys in the request data, require only 'name'",
        }

        # Test change vending machine name with 'name' argument not a list.
        data = {"name": "ven2"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "'name' argument must be a list of two name 'oldname' and 'newname'",
        }

        # Test change vending machine name with 'name' argument that contain more or less than 2 name.
        data = {"name": ["ven2", "ven3", "ven4"]}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "'name' argument must be a list of two name 'oldname' and 'newname'",
        }


def test_change_vending_machine_location_api() -> None:
    route = "/api/machine/change-location"
    with app.test_client() as client:
        data = {"name": "ven2", "location": "B"}
        response = client_post(client, route, data)
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "success": True,
            "message": {"name": "ven2", "location": "B", "items": {}},
        }

        # Test change vending machine location with not exist vending machine name
        data = {"name": "non-exist", "location": "C"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Vending machine with name 'non-exist' does not exists.",
        }

        # Test change vending machine location with new location that are same with old location.
        data = {"name": "ven2", "location": "B"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Old vending machine location: 'B' and new vending machine location: 'B' are the same",
        }

        # Test change vending machine location with missing some argument.
        data = {"name": "ven2"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Both 'name' and 'location' must be present in the request data",
        }

        # Test change vending machine name with excessive argument.
        data = {"name": "ven2", "location": "B", "items": {}}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Too many keys in the request data, require only 'name' and 'location'",
        }


def test_add_vending_machine_item_api() -> None:
    route = "/api/item/add-item"
    with app.test_client() as client:
        data = {"name": "ven2", "items": {"orio": 50}}
        response = client_post(client, route, data)
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "success": True,
            "message": {"name": "ven2", "location": "B", "items": {"orio": 50}},
        }

        # Add item to existing item, will increase amount.
        data = {"name": "ven2", "items": {"orio": 100}}
        response = client_post(client, route, data)
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "success": True,
            "message": {"name": "ven2", "location": "B", "items": {"orio": 150}},
        }

        # Test add vending machine item with not exist vending machine name
        data = {"name": "non-exist", "items": {"orio": 100}}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Vending machine with name 'non-exist' does not exists.",
        }

        # Test add vending machine item with missing argument.
        data = {"name": "ven2"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Both 'name' and 'items' must be present in the request data",
        }

        # Test add vending machine item with excessive argument.
        data = {"name": "ven2", "location": "b", "items": {"orio": 100}}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Too many keys in the request data, require only 'name' and 'items'",
        }

        # Test add vending machine item with excessive item.
        data = {"name": "ven2", "items": {"orio": 100, "drink": 50}}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Too many item to add, can be add one item at a time.",
        }


def test_edit_vending_machine_item_api():
    route = "/api/item/edit-item-amount"
    with app.test_client() as client:
        data = {"name": "ven2", "items": {"orio": 5000}}
        response = client_post(client, route, data)
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "success": True,
            "message": {"name": "ven2", "location": "B", "items": {"orio": 5000}},
        }

        # Test edit vending machine item with non int value of amount
        data = {"name": "ven2", "items": {"orio": "100"}}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Amount of an item must be int value",
        }

        # Test edit vending machine item with non exist vending machine name
        data = {"name": "non-exist", "items": {"orio": 100}}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Vending machine with name 'non-exist' does not exists.",
        }

        # Test edit vending machine item with non exist item
        data = {"name": "ven2", "items": {"non-exist": 100}}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Item with name 'non-exist' does not exists.",
        }

        # Test edit vending machine item with missing argument.
        data = {"name": "ven2"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Both 'name' and 'items' must be present in the request data",
        }

        # Test edit vending machine item with excessive argument.
        data = {"name": "ven2", "location": "b", "items": {"orio": 100}}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Too many keys in the request data, require only 'name' and 'items'",
        }

        # Test edit vending machine item with excessive item.
        data = {"name": "ven2", "items": {"orio": 100, "drink": 50}}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Too many item to edit, can be only edit one item at a time.",
        }


def test_remove_vending_machine_item_api() -> None:
    route = "/api/item/remove-item"
    with app.test_client() as client:
        data = {"name": "ven2", "items": "orio"}
        response = client_post(client, route, data)
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "success": True,
            "message": {"name": "ven2", "location": "B", "items": {}},
        }

        # Test remove vending machine item with non-exist vending machine name.
        data = {"name": "non-exist", "items": "orio"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Vending machine with name 'non-exist' does not exists.",
        }

        # Test remove vending machine item with non-exist item name.
        data = {"name": "ven2", "items": "non-exist"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Item with name 'non-exist' does not exists.",
        }

        # Test edit vending machine item with missing argument.
        data = {"name": "ven2"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Both 'name' and 'items' must be present in the request data",
        }

        # Test edit vending machine item with excessive argument.
        data = {"name": "ven2", "location": "b", "items": "orio"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Too many keys in the request data, require only 'name' and 'items'",
        }


def test_delete_vending_machine_by_name_api() -> None:
    route = "/api/machine/delete-machine"
    with app.test_client() as client:
        data = {"name": "ven2"}
        response = client_post(client, route, data)
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "success": True,
            "message": "Successfully, delete vending machine",
        }

        # Test delete vending machine with non-exist vending machine name
        data = {"name": "ven2"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Vending machine with name 'ven2' does not exists.",
        }

        # Test edit vending machine item with missing argument.
        data = {"location": "A"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Missing 'name' in the request data",
        }

        # Test edit vending machine item with excessive argument.
        data = {"name": "ven2", "location": "b", "items": "orio"}
        response = client_post(client, route, data)
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Too many keys in the request data",
        }
