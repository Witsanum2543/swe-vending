## Vending Machine Manager

This application provides an easy-to-use platform for managing of vending machine.
The application allows you to create and manage vending machine,
view their information, and track stock of each machine.

## Installation

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


## Usage (Supported APIs):

| API URL                               | METHOD           | DESCRIPTION                 |
|---------------------------------------|------------------|-----------------------------|
| `/api/machine/create-machine`   | **POST**         | Create new vending machine. |


## Tests

This project using [pytest](https://docs.pytest.org/en/latest/) for testing

### How to Run Tests

1. Make sure you have pytest installed, as listed in the `pyproject.toml` file or run `poetry install`
2. Run the command `pytest -v` in project's root directory to execute all test.

### Test Coverage

To measure the test coverage, run the command `pytest --cov=app` in the terminal. This will show you the percentage of the codebase that is covered by tests.
