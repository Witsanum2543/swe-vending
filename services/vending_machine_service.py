from tinydb import Query, TinyDB


class VendingMachineService:
    def __init__(self: "VendingMachineService", db: TinyDB) -> None:
        self.db = db

    def purge_database(self: "VendingMachineService") -> None:
        """
        Purge all data from the services.
        This function will remove all data from the services,
        effectively resetting it to its initial state.

        Returns:
            None
        """
        self.db.truncate()

    def create_new_vending_machine(
        self: "VendingMachineService", vending_machine_name: str, location: str
    ) -> dict:
        """
        Creates a new vending machine with the given name and location.

        Parameters:
            vending_machine_name (str): The name of the vending machine.
            location (str): The location of the vending machine.

        Raises:
            ValueError: If vending machine with the given name exist in the services.

        Returns:
            dict: A dictionary containing the information of the newly created vending machine, including the
            name, location, and items.
        """
        existing_machine = self.db.search(Query().name == vending_machine_name)
        if existing_machine:
            raise ValueError(
                f"Vending machine with name '{vending_machine_name}' already exists."
            )
        self.db.insert(
            {
                "name": vending_machine_name,
                "location": location,
                "items": {},
            }
        )
        return self.get_vending_machine_info(vending_machine_name)

    def get_vending_machine_info(
        self: "VendingMachineService", vending_machine_name: str
    ) -> dict:
        """
        Retrieves the information of a vending machine with the given name.

        Parameters:
            vending_machine_name (str): The name of the vending machine.

        Raises:
            ValueError: If vending machine with the given name does not exist.

        Returns:
            dict: A dictionary containing the information of the vending machine, including the name, location, and items.
        """
        existing_machine = self.db.search(Query().name == vending_machine_name)
        if not existing_machine:
            raise ValueError(
                f"Vending machine with name '{vending_machine_name}' does not exists."
            )
        return existing_machine[0]

    def get_all_vending_machine_info(self: "VendingMachineService") -> [dict]:
        """
        Retrieves all of a vending machine information in the database.

        Parameters:
            None

        Raises:
            ValueError: If vending machine with the given name does not exist.

        Returns:
            List[dict]: A List of dictionary containing the information of every vending machine in the database.
        """
        all_machine = self.db.all()
        return all_machine

    def change_vending_machine_name(
        self: "VendingMachineService",
        old_vending_machine_name: str,
        new_vending_machine_name: str,
    ) -> dict:
        """
        Update the name of a vending machine in the services.

        Parameters:
            old_vending_machine_name (str): The current name of the vending machine.
            new_vending_machine_name (str): The new name of the vending machine.

        Raises:
            ValueError: If the old and new vending machine names are the same.
            ValueError: If the vending machine with the old name does not exist in the services.

        Returns:
            dict: A dictionary containing the information of the newly vending machine name, including the
            name, location, and items.
        """
        existing_machine = self.db.search(Query().name == old_vending_machine_name)

        if not existing_machine:
            raise ValueError(
                f"Vending machine with name '{old_vending_machine_name}' does not exists."
            )

        if old_vending_machine_name == new_vending_machine_name:
            raise ValueError(
                f"Old vending machine name: '{old_vending_machine_name}' and new vending machine name: '{new_vending_machine_name}' are the same"
            )

        self.db.update(
            {"name": new_vending_machine_name},
            Query().name == old_vending_machine_name,
        )
        return self.get_vending_machine_info(new_vending_machine_name)

    def change_vending_machine_location(
        self: "VendingMachineService",
        vending_machine_name: str,
        new_vending_machine_location: str,
    ) -> dict:
        """
        Change the location of a vending machine in the services.

        Parameters:
            vending_machine_name (str): name of the vending machine to change location.
            new_vending_machine_location (str): new location for the vending machine.

        Raises:
            ValueError: If vending machine with the given name does not exist in the services.
            ValueError: If old location and new location are the same.

        Returns:
            dict: A dictionary containing the information of the newly vending machine location, including the
            name, location, and items.
        """
        existing_machine = self.db.search(Query().name == vending_machine_name)
        if not existing_machine:
            raise ValueError(
                f"Vending machine with name '{vending_machine_name}' does not exists."
            )

        old_location = existing_machine[0]["location"]
        if old_location == new_vending_machine_location:
            raise ValueError(
                f"Old vending machine location: '{old_location}' and new vending machine location: '{new_vending_machine_location}' are the same"
            )

        self.db.update(
            {"location": new_vending_machine_location},
            Query().name == vending_machine_name,
        )
        return self.get_vending_machine_info(vending_machine_name)

    def add_vending_machine_item(
        self: "VendingMachineService",
        vending_machine_name: str,
        item_name: str,
        add_amount: int,
    ) -> dict:
        """
        Add a specific item to a vending machine. If item already exist in the vending machine,
        it will add quantity to that item. If item not exist in the vending machine,
        it will add new item to the list of items.

        Parameters:
            vending_machine_name (str): The name of the vending machine to which the item will be added.
            item_name (str): The name of the item to be added to the vending machine.
            add_amount (int): The amount of the item to be added to the vending machine.

        Raises:
            ValueError: If vending machine with the given name does not exist in the services.

        Returns:
            dict: A dictionary containing the information of given vending machine, including the
            name, location, and items.
        """
        existing_machine = self.db.search(Query().name == vending_machine_name)
        if not existing_machine:
            raise ValueError(
                f"Vending machine with name '{vending_machine_name}' does not exists."
            )

        item_list = existing_machine[0]["items"]
        if item_name not in item_list:
            self.db.update(
                {"items": {item_name: add_amount}},
                Query().name == vending_machine_name,
            )
        else:
            old_item_amount = item_list[item_name]
            self.db.update(
                {"items": {item_name: old_item_amount + add_amount}},
                Query().name == vending_machine_name,
            )
        return self.get_vending_machine_info(vending_machine_name)

    def edit_vending_machine_item_amount(
        self: "VendingMachineService",
        vending_machine_name: str,
        item_name: str,
        amount: int,
    ) -> dict:
        """
        Edit a specific item in the vending machine.

        Parameters:
            vending_machine_name (str): The name of the vending machine to which the item will be edited.
            item_name (str): The name of the item to be edited.
            amount (int): The quantity of item that will be set.

        Raises:
            ValueError: If vending machine with the given name does not exist in the services.
            ValueError: If item with the given name does not exist in the vending machine.

        Returns:
            dict: A dictionary containing the information of given vending machine, including the
            name, location, and items.
        """
        if type(amount) != int:
            raise ValueError("Amount of an item must be int value")

        existing_machine = self.db.search(Query().name == vending_machine_name)
        if not existing_machine:
            raise ValueError(
                f"Vending machine with name '{vending_machine_name}' does not exists."
            )

        item_list = existing_machine[0]["items"]
        if item_name not in item_list:
            raise ValueError(f"Item with name '{item_name}' does not exists.")

        self.db.update(
            {"items": {item_name: amount}},
            Query().name == vending_machine_name,
        )
        return self.get_vending_machine_info(vending_machine_name)

    def remove_vending_machine_item(
        self: "VendingMachineService", vending_machine_name: str, item_name: str
    ) -> dict:
        """
        Remove a specific item from a vending machine.

        Parameters:
            vending_machine_name (str): The name of the vending machine to which the item will be removed.
            item_name (str): The name of the item to be removed.

        Raises:
            ValueError: If vending machine with the given name does not exist in the services.
            ValueError: If item with the given name does not exist in the vending machine.

        Returns:
            dict: A dictionary containing the information of given vending machine, including the
            name, location, and items.
        """
        existing_machine = self.db.search(Query().name == vending_machine_name)
        if not existing_machine:
            raise ValueError(
                f"Vending machine with name '{vending_machine_name}' does not exists."
            )

        item_list = existing_machine[0]["items"]
        if item_name not in item_list:
            raise ValueError(f"Item with name '{item_name}' does not exists.")

        del item_list[item_name]
        self.db.update({"items": item_list}, Query().name == vending_machine_name)
        return self.get_vending_machine_info(vending_machine_name)

    def delete_vending_machine_by_name(
        self: "VendingMachineService", vending_machine_name: str
    ) -> str:
        """
        Delete an existing vending machine with the given name.

        Parameters:
            vending_machine_name (str): The name of the vending machine.

        Raises:
            ValueError: If vending machine with the given name does not exist in the services.

        Returns:
            str: indicate whether it success
        """
        existing_machine = self.db.search(Query().name == vending_machine_name)
        if not existing_machine:
            raise ValueError(
                f"Vending machine with name '{vending_machine_name}' does not exists."
            )
        self.db.remove(Query().name == vending_machine_name)
        return "Successfully, delete vending machine"
