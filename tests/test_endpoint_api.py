import json

from app import app


def test_purge_database_api() -> None:
    with app.test_client() as client:
        response = client.get("/api/purge-database")
        assert response.status_code == 200


def test_create_vending_machine_api() -> None:
    with app.test_client() as client:
        data = {"name": "ven1", "location": "A"}
        response = client.post(
            "/api/machine/create-machine",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 200
        assert json.loads(response.data) == {
            "success": True,
            "message": {"name": "ven1", "location": "A", "items": {}},
        }

        # Test vending machine creation with existing name

        data = {"name": "ven1", "location": "B"}
        response = client.post(
            "/api/machine/create-machine",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Vending machine with name 'ven1' already exists.",
        }

        # Test vending machine creation with missing required parameters

        data = {"location": "A"}
        response = client.post(
            "/api/machine/create-machine",
            data=json.dumps(data),
            content_type="application/json",
        )
        assert response.status_code == 400
        assert json.loads(response.data) == {
            "success": False,
            "message": "Both 'name' and 'location' must be present in the request data",
        }
