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

#data = {"Name": "ven1", "location": "salaya", "items": {"orio": 20, "water": 10}}


# Create data
#database.child("vending-machine").child("ven1").set(data)


# Read data
#ven1 = database.child("vending-machine").child("ven1").get()
#print(ven1.val())


# Update data (JSON format)
# database.child("vending-machine").child("ven1").update({
#     "Name": "ven2",
# })

# Remove data
# Delete attribute of record
#database.child("vending-machine").child("ven1").child("Name").remove()
# Delete a record
#database.child("vending-machine").child("ven1").remove()

# ------------------------------------- USAGE FUNCTION ---------------------------------------------

"""
Create new vending machine in the database
"""
def createVendingMachine(vendingName: str, location: str, items: dict={}):
    vending = {
        "name": vendingName,
        "location": location,
        "items": items
    }
    database.child("vending-machine").child(vendingName).set(vending)

"""
Delete vending machine from the database
"""
def deleteVendingMachine(vendingName: str):
    database.child("vending-machine").child(vendingName).remove()

"""
Change name of vending machine
"""
def changeVendingName(oldName: str, newName: str):
    # get value from oldName record
    oldVen = database.child("vending-machine").child(oldName).get().val()
    # check if oldName vending machine is exist
    if oldVen == None:
        raise NameError(f'vending:{oldName} does not exist')
    else:
        # remove oldName record from database
        database.child("vending-machine").child(oldName).remove()
        # create newName record
        database.child("vending-machine").child(newName).set(oldVen)
        # change name to newName
        database.child("vending-machine").child(newName).update({"Name": newName})

"""
Change location of existing vending machine

parameter vendingName : name of vending machine
parameter newLocation : new location of vending machine
"""
def changeVendingLocation(vendingName: str, newLocation: str):
    database.child("vending-machine").child(vendingName).update({"Location": newLocation})

"""
Edit item in vending machine

parameter vendingName : name of vending machine
parameter itemName : name of an item that want to edit (must be exist item)
parameter amount : amount of item that want to set to
"""
def editVendingItem(vendingName: str, itemName: str, amount: int):
    item = database.child("vending-machine").child(vendingName).child("Items").child(itemName).get().val()
    if item == None:
        raise NameError(f'item:{itemName} does not exist')
    else:
        database.child("vending-machine").child(vendingName).child("Items").update({itemName: amount})

"""
Add item in vending machine

parameter vendingName : name of vending machine
parameter itemName : name of an item that want to added, could be new item or exist item
parameter amount : amount that want to add in
"""
def addVendingItem(vendingName: str, itemName: str, amount: int):
    itemsList = database.child("vending-machine").child(vendingName).child("Items").get()
    oldAmount = itemsList.val().get(itemName)
    if oldAmount != None:
        database.child("vending-machine").child(vendingName).child("Items").update({itemName: oldAmount + amount})
    else:
        database.child("vending-machine").child(vendingName).child("Items").update({itemName: amount})

"""
Remove item from vending machine

parameter vendingName : name of vending machine
parameter itemName : name of an item that want to remove
"""
def removeVendingItem(vendingName: str, itemName: str):
    database.child("vending-machine").child(vendingName).child("Items").child(itemName).remove()

"""
Get vendingMachine information
return : JSON format
"""
def getVendingMachine(vendingName: str):
    if database.child("vending-machine").child(vendingName).get().val() == None:
        raise NameError(f'vending:{vendingName} does not exist')
    else:
        return database.child("vending-machine").child(vendingName).get().val()

# ------------------------------------- API ---------------------------------------------

# Create vending machine API
# receive format example
# {
#     "name":"ven",
#     "location":"a",
#     "items": {"orio":50, "water":10}
# }
@app.route("/create", methods=['POST'])
def create():
    data = request.get_json('name') # somehow there must have some string inside () to make it work
    vendingName = data['name']
    location = data['location']
    items = data['items']
    createVendingMachine(vendingName, location, items)
    return getVendingMachine(vendingName)

# Delete vending machine by name API
# receive format as 'form-data'
# KEY : vendingName , VALUE : ...
@app.route("/deleteByName", methods=['POST'])
def deleteByName():
    vendingName = request.form['vendingName']
    deleteVendingMachine(vendingName)
    return f'Successfully delete {vendingName}'

# Change vending machine name API
# receive format as 'form-data'
# KEY : oldName , VALUE : ...
# KEY : newName , VALUE : ...
@app.route("/changeName", methods=['POST'])
def changeName():
    oldName = request.form['oldName']
    newName = request.form['newName']
    changeVendingName(oldName, newName)
    return f'Successfully change name from {oldName} to {newName}'

# Change vending machine name API
# receive format as 'form-data'
# KEY : vendingName , VALUE : ...
# KEY : location , VALUE : ...
@app.route("/changeLocation", methods=['POST'])
def changeLocation():
    vendingName = request.form['vendingName']
    location = request.form['location']
    changeVendingLocation(vendingName, location)
    return f'Successfully change location of {vendingName} to {location}'

# Edit item API
# receive format as 'form-data'
# KEY : vendingName , VALUE : ...
# KEY : itemName , VALUE : ...
# KEY : amount , VALUE : ...
@app.route("/editItem", methods=['POST'])
def editItem():
    vendingName = request.form['vendingName']
    itemName = request.form['itemName']
    amount = int(request.form['amount'])
    editVendingItem(vendingName, itemName, amount)
    return getVendingMachine(vendingName)

# Add item API
# receive format as 'form-data'
# KEY : vendingName , VALUE : ...
# KEY : itemName , VALUE : ...
# KEY : amount , VALUE : ...
@app.route("/addItem", methods=['POST'])
def addItem():
    vendingName = request.form['vendingName']
    itemName = request.form['itemName']
    amount = int(request.form['amount'])
    addVendingItem(vendingName, itemName, amount)
    return getVendingMachine(vendingName)

# Remove item API
# receive format as 'form-data'
# KEY : vendingName , VALUE : ...
# KEY : itemName , VALUE : ...
@app.route("/removeItem", methods=['POST'])
def removeItem():
    vendingName = request.form['vendingName']
    itemName = request.form['itemName']
    removeVendingItem(vendingName, itemName)
    return getVendingMachine(vendingName)

# Get vending machine by name API
# receive format as 'form-data'
# KEY : vendingName , VALUE : ...
@app.route("/getByName", methods=['POST'])
def getByName():
    vendingName = request.form['vendingName']
    return getVendingMachine(vendingName)

# Get all vending machine API
@app.route("/getAll", methods=['GET'])
def getAll():
    return database.child("vending-machine").get().val()

# run app on port 8080 in debug mode
if __name__ == "__main__":
    app.run(debug=True, port=8080) 