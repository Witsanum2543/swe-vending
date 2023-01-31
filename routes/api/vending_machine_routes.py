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


@vending_machine_controller.route("/machine/create-machine", methods=["POST"])
def create_vending_machine_api() -> tuple[Response, int]:
    request_json_data = request.get_json("name")

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


# @app.route("/delete-vending-machine-by-name", methods=['POST'])
# def delete_vending_machine_by_name_api():
#     vending_machine_name = request.form['vendingName']
#
#     delete_vending_machine_by_name(vending_machine_name)
#     return f'Successfully delete {vending_machine_name}'
#
#
# """
# receive format as 'form-data'
# KEY : oldName , VALUE : ...
# KEY : newName , VALUE : ...
# """
#
# @app.route("/change-vending-machine-name-api", methods=['POST'])
# def change_vending_machine_name_api():
#     old_vending_machine_name = request.form['oldName']
#     new_vending_machine_name = request.form['newName']
#
#     change_vending_machine_name(old_vending_machine_name, new_vending_machine_name)
#     return f'Successfully change name from {old_vending_machine_name} to {new_vending_machine_name}'
#
#
# """
# receive format as 'form-data'
# KEY : vendingName , VALUE : ...
# KEY : location , VALUE : ...
# """
#
# @app.route("/change-vending-machine-location-api", methods=['POST'])
# def change_vending_machine_location_api():
#     vending_machine_name = request.form['vendingName']
#     location = request.form['location']
#
#     change_vending_machine_location(vending_machine_name, location)
#     return f'Successfully change location of {vending_machine_name} to {location}'
#
#
# """
# receive format as 'form-data'
# KEY : vendingName , VALUE : ...
# KEY : itemName , VALUE : ...
# KEY : amount , VALUE : ...
# """
#
# @app.route("/edit-vending-machine-item-amount-api", methods=['POST'])
# def edit_vending_machine_item_amount_api():
#     vending_machine_name = request.form['vendingName']
#     item_name = request.form['itemName']
#     amount = int(request.form['amount'])
#
#     edit_vending_machine_item_amount(vending_machine_name, item_name, amount)
#     return get_vending_machine_info(vending_machine_name)
#
#
# """
# receive format as 'form-data'
# KEY : vendingName , VALUE : ...
# KEY : itemName , VALUE : ...
# KEY : amount , VALUE : ...
# """
#
#
# @app.route("/add-vending-machine-item-api", methods=['POST'])
# def add_vending_machine_item_api():
#     vending_machine_name = request.form['vendingName']
#     item_name = request.form['itemName']
#     amount = int(request.form['amount'])
#
#     add_vending_machine_item(vending_machine_name, item_name, amount)
#     return get_vending_machine_info(vending_machine_name)
#
#
# """
# receive format as 'form-data'
# KEY : vendingName , VALUE : ...
# KEY : itemName , VALUE : ...
# """
#
#
# @app.route("/remove-vending-machine-item-api", methods=['POST'])
# def remove_vending_machine_item_api():
#     vending_machine_name = request.form['vendingName']
#     item_name = request.form['itemName']
#
#     remove_vending_machine_item(vending_machine_name, item_name)
#     return get_vending_machine_info(vending_machine_name)
#
#
# """
# receive format as 'form-data'
# KEY : vendingName , VALUE : ...
# """
#
# @app.route("/get-vending-machine-info-api", methods=['POST'])
# def get_vending_machine_info_api():
#     vending_machine_name = request.form['vendingName']
#
#     return get_vending_machine_info(vending_machine_name)
#
#
# @app.route("/get-all-vending-machine-info-api", methods=['GET'])
# def get_all_vending_machine_info_api():
#     return services.child("vending-machine").get().val()
#
#
