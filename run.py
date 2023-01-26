import pyrebase
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

config = {
    "apiKey": "AIzaSyB9MKaALpw2j8XiPvPmBWpehSro-ZJhrnw",
    "authDomain": "swe-vending-machine.firebaseapp.com",
    "projectId": "swe-vending-machine",
    "storageBucket": "swe-vending-machine.appspot.com",
    "messagingSenderId": "256757566088",
    "appId": "1:256757566088:web:bc0021a5d2acabe8dbad3d",
    "measurementId": "G-8PSK5BJBJE",
    "databaseURL": "https://swe-vending-machine-default-rtdb.asia-southeast1.firebasedatabase.app/",
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()


# ------------------------------------- USAGE FUNCTION ---------------------------------------------

def create_new_vending_machine(vending_machine_name: str, location: str, items: dict = {}):
    new_vending = {
        "name": vending_machine_name,
        "location": location,
        "items": items
    }
    database.child("vending-machine").child(vending_machine_name).set(new_vending)


def delete_vending_machine_by_name(vending_machine_name: str):
    database.child("vending-machine").child(vending_machine_name).remove()


def change_vending_machine_name(old_vending_machine_name: str, new_vending_machine_name: str):
    old_vending_machine = database.child("vending-machine").child(old_vending_machine_name).get().val()

    if old_vending_machine is None:
        raise NameError(f'vending:{old_vending_machine_name} does not exist')
    else:
        # remove old_vending_machine record from database
        database.child("vending-machine").child(old_vending_machine_name).remove()
        # create new vending machine record with old vending machine information
        database.child("vending-machine").child(new_vending_machine_name).set(old_vending_machine)
        # change name to new_vending_machine_name
        database.child("vending-machine").child(new_vending_machine_name).update({"Name": new_vending_machine_name})


def change_vending_machine_location(vending_machine_name: str, new_vending_machine_location: str):
    database.child("vending-machine").child(vending_machine_name).update({"Location": new_vending_machine_location})


def edit_vending_machine_item_amount(vending_machine_name: str, item_name: str, amount: int):
    item = database.child("vending-machine").child(vending_machine_name).child("Items").child(item_name).get().val()

    if item is None:
        raise NameError(f'item:{item_name} does not exist')
    else:
        database.child("vending-machine").child(vending_machine_name).child("Items").update({item_name: amount})


def add_vending_machine_item(vending_machine_name: str, item_name: str, add_amount: int):
    items_list = database.child("vending-machine").child(vending_machine_name).child("Items").get()
    item_amount = items_list.val().get(item_name)
    if item_amount is None:
        database.child("vending-machine").child(vending_machine_name).child("Items").update(
            {item_name: item_amount + add_amount})
    else:
        database.child("vending-machine").child(vending_machine_name).child("Items").update({item_name: add_amount})


def remove_vending_machine_item(vending_machine_name: str, item_name: str):
    database.child("vending-machine").child(vending_machine_name).child("Items").child(item_name).remove()


def get_vending_machine_info(vending_machine_name: str):
    if database.child("vending-machine").child(vending_machine_name).get().val() is None:
        raise NameError(f'vending:{vending_machine_name} does not exist')
    else:
        return database.child("vending-machine").child(vending_machine_name).get().val()


# ------------------------------------- API ---------------------------------------------

"""
receive format example
{
    "name":"ven",
    "location":"a",
    "items": {"orio":50, "water":10}
}
"""


@app.route("/create-vending-machine", methods=['POST'])
def create_vending_machine_api():
    request_json_data = request.get_json('name')  # somehow there must have some string inside () to make it return

    vending_machine_name = request_json_data['name']
    location = request_json_data['location']
    items = request_json_data['items']

    create_new_vending_machine(vending_machine_name, location, items)
    return get_vending_machine_info(vending_machine_name)


"""
receive format as 'form-data'
KEY : vendingName , VALUE : ...
"""


@app.route("/delete-vending-machine-by-name", methods=['POST'])
def delete_vending_machine_by_name_api():
    vending_machine_name = request.form['vendingName']

    delete_vending_machine_by_name(vending_machine_name)
    return f'Successfully delete {vending_machine_name}'


"""
receive format as 'form-data'
KEY : oldName , VALUE : ...
KEY : newName , VALUE : ...
"""

@app.route("/change-vending-machine-name-api", methods=['POST'])
def change_vending_machine_name_api():
    old_vending_machine_name = request.form['oldName']
    new_vending_machine_name = request.form['newName']

    change_vending_machine_name(old_vending_machine_name, new_vending_machine_name)
    return f'Successfully change name from {old_vending_machine_name} to {new_vending_machine_name}'


"""
receive format as 'form-data'
KEY : vendingName , VALUE : ...
KEY : location , VALUE : ...
"""

@app.route("/change-vending-machine-location-api", methods=['POST'])
def change_vending_machine_location_api():
    vending_machine_name = request.form['vendingName']
    location = request.form['location']

    change_vending_machine_location(vending_machine_name, location)
    return f'Successfully change location of {vending_machine_name} to {location}'


"""
receive format as 'form-data'
KEY : vendingName , VALUE : ...
KEY : itemName , VALUE : ...
KEY : amount , VALUE : ...
"""

@app.route("/edit-vending-machine-item-amount-api", methods=['POST'])
def edit_vending_machine_item_amount_api():
    vending_machine_name = request.form['vendingName']
    item_name = request.form['itemName']
    amount = int(request.form['amount'])

    edit_vending_machine_item_amount(vending_machine_name, item_name, amount)
    return get_vending_machine_info(vending_machine_name)


"""
receive format as 'form-data'
KEY : vendingName , VALUE : ...
KEY : itemName , VALUE : ...
KEY : amount , VALUE : ...
"""


@app.route("/add-vending-machine-item-api", methods=['POST'])
def add_vending_machine_item_api():
    vending_machine_name = request.form['vendingName']
    item_name = request.form['itemName']
    amount = int(request.form['amount'])

    add_vending_machine_item(vending_machine_name, item_name, amount)
    return get_vending_machine_info(vending_machine_name)


"""
receive format as 'form-data'
KEY : vendingName , VALUE : ...
KEY : itemName , VALUE : ...
"""


@app.route("/remove-vending-machine-item-api", methods=['POST'])
def remove_vending_machine_item_api():
    vending_machine_name = request.form['vendingName']
    item_name = request.form['itemName']

    remove_vending_machine_item(vending_machine_name, item_name)
    return get_vending_machine_info(vending_machine_name)


"""
receive format as 'form-data'
KEY : vendingName , VALUE : ...
"""

@app.route("/get-vending-machine-info-api", methods=['POST'])
def get_vending_machine_info_api():
    vending_machine_name = request.form['vendingName']

    return get_vending_machine_info(vending_machine_name)


@app.route("/get-all-vending-machine-info-api", methods=['GET'])
def get_all_vending_machine_info_api():
    return database.child("vending-machine").get().val()


# run app on port 8080 in debug mode
if __name__ == "__main__":
    app.run(debug=True, port=8080)
