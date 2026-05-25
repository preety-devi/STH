from storage import load_inventory, save_inventory


inventory = load_inventory()


def generate_item_id():
    if not inventory:
        return 1

    max_id = max(item["item_id"] for item in inventory)
    return max_id + 1


def add_item():
    item_name = input("Enter item name: ").strip()

    if not item_name:
        print("Item name cannot be empty.")
        return

    try:
        quantity = int(input("Enter quantity: "))

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

    print("\nInventory Items:\n")

    for item in inventory:
        print(f"ID: {item['item_id']}")
        print(f"Item: {item['item_name']}")
        print(f"Quantity: {item['quantity']}")
        print("-" * 20)


def update_quantity():
    try:
        item_id = int(input("Enter item ID: "))

    except ValueError:
        print("Invalid item ID.")
        return

    for item in inventory:
        if item["item_id"] == item_id:

            try:
                new_quantity = int(input("Enter new quantity: "))

                if new_quantity < 0:
                    print("Quantity cannot be negative.")
                    return

            except ValueError:
                print("Please enter a valid number.")
                return

            item["quantity"] = new_quantity

            save_inventory(inventory)

            print("Quantity updated successfully.")
            return

    print("Item not found.")