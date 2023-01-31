from tinydb import TinyDB


def get_db(path: str) -> TinyDB:
    db = TinyDB(path + "db.json")
    return db


def get_test_db(path: str) -> TinyDB:
    test_db = TinyDB(path + "test_db.json")
    return test_db
