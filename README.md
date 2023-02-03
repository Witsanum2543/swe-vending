# Vending Machine Manager

This application provides an easy-to-use platform for managing of vending machine.
The application allows you to create and manage vending machine,
view their information, and track stock of each machine.

# Installation

1. install [Poetry](https://python-poetry.org/docs/)
2. Clone the repository
```bash
git clone https://github.com/Witsanum2543/swe-vending.git
```
3. Install the dependencies inside project directory
```bash
poetry install
```
4. Create a .env file in the root directory of the project and set the following environment variables:
```bash
DB_PATH='./database/'
TEST_DB_PATH='../database/'
```
5. run app.py in the root directory
```bash
python app.py
```


# Usage (Supported APIs):

| API URL                      | METHOD   | DESCRIPTION                                                        | JSON EXPECTATION  |
|------------------------------|----------|--------------------------------------------------------------------|-------------------|
| `/api/purge-database`        | **GET**  | Reset all data from database.                                      | None              |
| `/api/machine/create-machine` | **POST** | Create new vending machine.                                        | [go there](#L63)  |
| `/api/machine/delete-machine` | **POST** | Delete an existing vending machine with the given name.          | [go there](#L70)  |
| `/api/machine/get-machine`   | **POST** | Retrieves the information of a vending machine with the given name. | [go there](#L76)  |
| `/api/machine/get-all-machine` | **GET**  | Retrieves all of a vending machine information in the database.    | None              |
| `/api/machine/change-name`   | **POST** | Update the name of a vending machine in the services.              | [go there](#L82)  |
| `/api/machine/change-location` | **POST** | Change the location of a vending machine in the services.          | [go there](#L88)  |
| `/api/item/add-item`         | **POST** | Add a specific item to a vending machine.                          | [go there](#L95)  |
| `/api/edit-item-amount` | **POST** | Edit a specific item in the vending machine.          | [go there](#L103) |
| `/api/item/remove-item` | **POST** | Remove a specific item from a vending machine.          | [go there](#L110) |



# Tests

This project using [pytest](https://docs.pytest.org/en/latest/) for testing

### How to Run Tests

1. Make sure you have pytest installed, as listed in the `pyproject.toml` file or run `poetry install`
2. Run the command `pytest -v` in project's root directory to execute all test.

### Test Coverage

To measure the test coverage, run the command `pytest --cov=app` in the terminal. This will show you the percentage of the codebase that is covered by tests.


# JSON Expectations
> _**NOTE**_: if you using postman to sending request you need to set Headers's `Content-Type` to `application/json`

- `/api/machine/create-machine`
  - ```JSON
      {
        "name": "vending_machine_name",
        "location": "vending_machine_location"
      }
      ```
- `/api/machine/delete-machine`
    - ```JSON
      {
        "name": "vending_machine_name"
      }
      ```
- `/api/machine/get-machine`
    - ```JSON
      {
        "name": "vending_machine_name"
      }
      ```
- `/api/machine/change-name`
    - ```JSON
      {
        "name": ["old_vending_machine_name", "new_vending_machine_name"]
      }
      ```
- `/api/machine/change-location`
    - ```JSON
      {
        "name": "vending_machine_name",
        "location": "new_vending_machine_location"
      }
      ```
- `/api/item/add-item`
    - Note: If you add item that never exist before, it will add that item to the items list.
    - ```JSON
      {
        "name": "vending_machine_name",
        "items": {"item_name":  amount}
      }
      ```
- `/api/edit-item-amount`
    - ```JSON
      {
        "name": "vending_machine_name",
        "items": {"item_name":  amount}
      }
      ```
- `/api/item/remove-item`
    - ```JSON
      {
        "name": "vending_machine_name",
        "items": "item_name"
      }
      ```
