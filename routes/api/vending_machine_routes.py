import os

from dotenv import load_dotenv
from flask import Blueprint, Response, jsonify, request

from database.db_manager import get_db
from services.vending_machine_service import VendingMachineService

vending_machine_controller = Blueprint(
    "vending_machine_controller", __name__, url_prefix="/api"
)

load_dotenv()
db = get_db(os.getenv("DB_PATH"))
machine_service = VendingMachineService(db)


@vending_machine_controller.route("/purge-database", methods=["GET"])
def purge_database_api() -> tuple[Response, int]:
    try:
        machine_service.purge_database()
        return jsonify(success=True, message="Successfully, reset database"), 200
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500


@vending_machine_controller.route("/machine/create-machine", methods=["POST"])
def create_vending_machine_api() -> tuple[Response, int]:
    request_json_data = request.get_json()

    if "name" not in request_json_data or "location" not in request_json_data:
        return (
            jsonify(
                success=False,
                message="Both 'name' and 'location' must be present in the request data",
            ),
            400,
        )

    if len(request_json_data) > 2:
        return (
            jsonify(
                success=False,
                message="Too many keys in the request data, require only 'name' and 'location'",
            ),
            400,
        )

    vending_machine_name = request_json_data["name"]
    location = request_json_data["location"]

    try:
        vending_machine = machine_service.create_new_vending_machine(
            vending_machine_name, location
        )
        return jsonify(success=True, message=vending_machine), 200
    except ValueError as ve:
        return jsonify(success=False, message=str(ve)), 400
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500


@vending_machine_controller.route("/machine/delete-machine", methods=["POST"])
def delete_vending_machine_by_name_api() -> tuple[Response, int]:
    request_json_data = request.get_json()

    if "name" not in request_json_data:
        return jsonify(success=False, message="Missing 'name' in the request data"), 400

    if len(request_json_data) > 1:
        return jsonify(success=False, message="Too many keys in the request data"), 400

    vending_machine_name = request_json_data["name"]

    try:
        ret_message = machine_service.delete_vending_machine_by_name(
            vending_machine_name
        )
        return jsonify(success=True, message=ret_message), 200
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500


@vending_machine_controller.route("/machine/change-name", methods=["POST"])
def change_vending_machine_name_api() -> tuple[Response, int]:
    request_json_data = request.get_json()

    if "name" not in request_json_data:
        return jsonify(success=False, message="Missing 'name' in the request data"), 400

    if len(request_json_data) > 1:
        return (
            jsonify(
                success=False,
                message="Too many keys in the request data, require only 'name'",
            ),
            400,
        )

    vending_machine_name = request_json_data["name"]

    try:
        vending_machine = machine_service.change_vending_machine_name(
            vending_machine_name
        )
        return jsonify(success=True, message=vending_machine), 200
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500


@vending_machine_controller.route("/machine/change-location", methods=["POST"])
def change_vending_machine_location_api() -> tuple[Response, int]:
    request_json_data = request.get_json()

    if "name" not in request_json_data or "location" not in request_json_data:
        return (
            jsonify(
                success=False,
                message="Both 'name' and 'location' must be present in the request data",
            ),
            400,
        )

    if len(request_json_data) > 2:
        return (
            jsonify(
                success=False,
                message="Too many keys in the request data, require only 'name' and 'location'",
            ),
            400,
        )

    vending_machine_name = request_json_data["name"]
    vending_machine_location = request_json_data["location"]

    try:
        vending_machine = machine_service.change_vending_machine_location(
            vending_machine_name, vending_machine_location
        )
        return jsonify(success=True, message=vending_machine), 200
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500


@vending_machine_controller.route("/item/edit-item-amount", methods=["POST"])
def edit_vending_machine_item_amount_api() -> tuple[Response, int]:
    request_json_data = request.get_json()

    if "name" not in request_json_data or "items" not in request_json_data:
        return (
            jsonify(
                success=False,
                message="Both 'name' and 'items' must be present in the request data",
            ),
            400,
        )

    if len(request_json_data) > 2:
        return (
            jsonify(
                success=False,
                message="Too many keys in the request data, require only 'name' and 'items'",
            ),
            400,
        )

    vending_machine_name = request_json_data["name"]
    vending_machine_items = request_json_data["items"]

    if len(vending_machine_items) > 1:
        return (
            jsonify(
                success=False,
                message="Too many item to edit, can be only edit one item at a time.",
            ),
            400,
        )

    item_name = list(vending_machine_items.keys())[0]
    item_amount = vending_machine_items[item_name]

    try:
        vending_machine = machine_service.edit_vending_machine_item_amount(
            vending_machine_name, item_name, item_amount
        )
        return jsonify(success=True, message=vending_machine), 200
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500


@vending_machine_controller.route("/item/add-item", methods=["POST"])
def add_vending_machine_item_api() -> tuple[Response, int]:
    request_json_data = request.get_json()

    if "name" not in request_json_data or "items" not in request_json_data:
        return (
            jsonify(
                success=False,
                message="Both 'name' and 'items' must be present in the request data",
            ),
            400,
        )

    if len(request_json_data) > 2:
        return (
            jsonify(
                success=False,
                message="Too many keys in the request data, require only 'name' and 'items'",
            ),
            400,
        )

    vending_machine_name = request_json_data["name"]
    vending_machine_items = request_json_data["items"]

    if len(vending_machine_items) > 1:
        return (
            jsonify(
                success=False,
                message="Too many item to add, can be add one item at a time.",
            ),
            400,
        )

    item_name = list(vending_machine_items.keys())[0]
    item_amount = vending_machine_items[item_name]

    try:
        vending_machine = machine_service.add_vending_machine_item(
            vending_machine_name, item_name, item_amount
        )
        return jsonify(success=True, message=vending_machine), 200
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500


@vending_machine_controller.route("/item/remove-item", methods=["POST"])
def remove_vending_machine_item_api() -> tuple[Response, int]:
    request_json_data = request.get_json()

    if "name" not in request_json_data or "items" not in request_json_data:
        return (
            jsonify(
                success=False,
                message="Both 'name' and 'items' must be present in the request data",
            ),
            400,
        )

    if len(request_json_data) > 2:
        return (
            jsonify(
                success=False,
                message="Too many keys in the request data, require only 'name' and 'items'",
            ),
            400,
        )

    vending_machine_name = request_json_data["name"]
    item_name = request_json_data["items"]

    try:
        vending_machine = machine_service.remove_vending_machine_item(
            vending_machine_name, item_name
        )
        return jsonify(success=True, message=vending_machine), 200
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500


@vending_machine_controller.route("/machine/get-machine", methods=["POST"])
def get_vending_machine_info_api() -> tuple[Response, int]:
    request_json_data = request.get_json()

    if "name" not in request_json_data:
        return jsonify(success=False, message="Missing 'name' in the request data"), 400

    if len(request_json_data) > 1:
        return (
            jsonify(
                success=False,
                message="Too many keys in the request data, require only 'name'",
            ),
            400,
        )

    vending_machine_name = request_json_data["name"]

    try:
        vending_machine = machine_service.get_vending_machine_info(vending_machine_name)
        return jsonify(success=True, message=vending_machine), 200
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500


@vending_machine_controller.route("/machine/get-all-machine", methods=["GET"])
def get_all_vending_machine_info_api() -> tuple[Response, int]:
    try:
        all_vending_machine = machine_service.get_all_vending_machine_info()
        return jsonify(success=True, message=all_vending_machine), 200
    except Exception as e:
        return jsonify(success=False, message=str(e)), 500
