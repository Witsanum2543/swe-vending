import os
import types

from dotenv import load_dotenv

from database.db_manager import get_test_db
from services import vending_machine_service

load_dotenv()

db = None
machine_service = None


def setup_module(module: types.ModuleType) -> None:
    global db, machine_service
    db = get_test_db(os.getenv("TEST_DB_PATH"))
    machine_service = vending_machine_service.VendingMachineService(db)
    machine_service.purge_database()


def test_create_new_vending_machine() -> None:
    vending_machine = machine_service.create_new_vending_machine("ven1", "a")
    assert vending_machine["name"] == "ven1"
    assert vending_machine["location"] == "a"
    assert vending_machine["items"] == {}


def test_get_vending_machine_info() -> None:
    vending_machine_name = "ven1"
    vending_machine = machine_service.get_vending_machine_info(vending_machine_name)
    assert vending_machine["name"] == "ven1"
    assert vending_machine["location"] == "a"
    assert vending_machine["items"] == {}


def test_change_vending_machine_name() -> None:
    old_vending_machine_name = "ven1"
    new_vending_machine_name = "ven2"
    vending_machine = machine_service.change_vending_machine_name(
        old_vending_machine_name, new_vending_machine_name
    )
    assert vending_machine["name"] == "ven2"


def test_change_vending_machine_location() -> None:
    vending_machine_name = "ven2"
    vending_machine_location = "B"
    vending_machine = machine_service.change_vending_machine_location(
        vending_machine_name, vending_machine_location
    )
    assert vending_machine["location"] == "B"


def test_add_vending_machine_item() -> None:
    vending_machine_name = "ven2"
    item_name = "orio"
    add_amount = 50
    vending_machine = machine_service.add_vending_machine_item(
        vending_machine_name, item_name, add_amount
    )
    assert vending_machine["items"][item_name] == 50


def test_edit_vending_machine_item_amount() -> None:
    vending_machine_name = "ven2"
    item_name = "orio"
    amount = 500
    vending_machine = machine_service.edit_vending_machine_item_amount(
        vending_machine_name, item_name, amount
    )
    assert vending_machine["items"][item_name] == 500


def test_remove_vending_machine_item() -> None:
    vending_machine_name = "ven2"
    item_name = "orio"
    vending_machine = machine_service.remove_vending_machine_item(
        vending_machine_name, item_name
    )
    assert (item_name in vending_machine["items"]) is False


def test_delete_vending_machine_by_name() -> None:
    vending_machine_name = "ven2"
    message = machine_service.delete_vending_machine_by_name(vending_machine_name)
    assert message == "Successfully, delete vending machine"


def teardown_module(module: types.ModuleType) -> None:
    machine_service.purge_database()
