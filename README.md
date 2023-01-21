## How to use :

1. run homework.py in terminal
```bash
python .\homework.py
```
2. url is "localhost:8080/"

## Tech Stack :

1. using Firebase for the database
2. using Flask

## Installation

installing pyrebase for Firebase API

```bash
pip install Pyrebase4
```

## Usage (Available URL):

1. "/create" (POST METHOD) - receive format as JSON raw
     {
        "name":"ven",
        "location":"a",
        "items": {"orio":50, "water":10}
     }

2. "/deleteByName" (POST METHOD) - receive format as 'form-data'
    KEY : vendingName , VALUE : name of vending machine that want to delete

3. "/changeName" (POST METHOD) - receive format as 'form-data'
    KEY : oldName , VALUE : name of vending machine that want to change name
    KEY : newName , VALUE : new name that want to assign to that vending machine

4. "/changeLocation" (POST METHOD) - receive format as 'form-data'
    KEY : vendingName , VALUE : name of vending machine that want to change location
    KEY : location , VALUE : new location that want to assign to that vending machine

5. "/editItem" (POST METHOD) - receive format as 'form-data'
    KEY : vendingName , VALUE : name of vending machine that want to edit item
    KEY : itemName , VALUE : name of an item that want to edit amount
    KEY : amount , VALUE : new amount of that item

6. "/addItem" (POST METHOD) - receive format as 'form-data' (can added new item that not exist or just add amount of existence item)
    KEY : vendingName , VALUE : name of vending machine that want to add item
    KEY : itemName , VALUE : name of an item that want to add 
    KEY : amount , VALUE : amount of that item that want to add

7. "/removeItem" (POST METHOD) - receive format as 'form-data'
    KEY : vendingName , VALUE : name of vending machine that want to remove item
    KEY : itemName , VALUE : name of item that want to remove

8. "/getByName" (POST METHOD) - receive format as 'form-data'
    KEY : vendingName , VALUE : name of vending machine that want to get information

9. "/getAll" (GET METHOD)
    return : JSON format of all vending machine information