from storage import load_inventory, save_inventory

inventory = load_inventory()


def generate_item_id():

    if not inventory:
        return 1

    max_id = max(item["item_id"] for item in inventory)

    return max_id + 1


def find_item_by_name(search_name):

    matches = []

    for item in inventory:

        if search_name.lower() in item["item_name"].lower():
            matches.append(item)

    return matches


def add_item():

    item_name = input("Enter item name: ").strip()

    if not item_name:
        print("Item name cannot be empty.")
        return

    try:
        quantity = int(
            input("Enter quantity (example: 100): ")
        )

        if quantity < 0:
            print("Quantity cannot be negative.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    item = {
        "item_id": generate_item_id(),
        "item_name": item_name,
        "quantity": quantity
    }

    inventory.append(item)

    save_inventory(inventory)

    print("Item added successfully.")


def view_items():

    if not inventory:
        print("No inventory items found.")
        return

    print("\nInventory Items:")

    for item in inventory:

        print(f"ID: {item['item_id']}")
        print(f"Item: {item['item_name']}")
        print(f"Quantity: {item['quantity']}")
        print("-" * 20)


def search_items():

    if not inventory:
        print("No inventory items found.")
        return

    search_name = input(
        "Enter item name to search: "
    ).strip()

    matches = find_item_by_name(search_name)

    if not matches:
        print("No matching item found.")

        print("\nCurrent Inventory:")
        view_items()

        return

    print("\nSearch Results:")

    for item in matches:

        print(f"ID: {item['item_id']}")
        print(f"Item: {item['item_name']}")
        print(f"Quantity: {item['quantity']}")
        print("-" * 20)


def update_quantity():

    print("\nCurrent Inventory:")
    view_items()

    search_name = input(
        "\nEnter item name to update: "
    ).strip()

    matches = find_item_by_name(search_name)

    if not matches:

        print("No matching item found.")

        print("\nCurrent Inventory:")
        view_items()

        return

    print("\nMatching Items:")

    for index, item in enumerate(matches, start=1):

        print(
            f"{index}. "
            f"{item['item_name']} "
            f"(Current Quantity: {item['quantity']})"
        )

    try:
        choice = int(
            input("Enter choice number: ")
        )

        if choice < 1 or choice > len(matches):
            print("Invalid choice.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    selected_item = matches[choice - 1]

    try:
        new_quantity = int(
            input(
                "Enter new quantity (example: 120): "
            )
        )

        if new_quantity < 0:
            print("Quantity cannot be negative.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    selected_item["quantity"] = new_quantity

    save_inventory(inventory)

    print("Quantity updated successfully.")

def delete_item():

    print("\nCurrent Inventory:")
    view_items()

    search_name = input(
        "\nEnter item name to delete: "
    ).strip()

    matches = find_item_by_name(search_name)

    if not matches:

        print("No matching item found.")

        print("\nCurrent Inventory:")
        view_items()

        return

    print("\nMatching Items:")

    for index, item in enumerate(matches, start=1):

        print(
            f"{index}. "
            f"{item['item_name']} "
            f"(Quantity: {item['quantity']})"
        )

    try:
        choice = int(
            input("Enter choice number: ")
        )

        if choice < 1 or choice > len(matches):
            print("Invalid choice.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    selected_item = matches[choice - 1]

    confirm = input(
        "Are you sure you want to delete this item? (y/n): "
    ).lower()

    if confirm != "y":
        print("Delete cancelled.")
        return

    inventory.remove(selected_item)

    save_inventory(inventory)

    print("Item deleted successfully.")