from storage import load_inventory, save_inventory

inventory = load_inventory()


def generate_item_id():
    if not inventory:
        return 1
    return max(item["item_id"] for item in inventory) + 1


def find_item_by_name(search_name):
    return [
        item for item in inventory
        if search_name.lower() in item["item_name"].lower()
    ]



def add_item():

    item_name = input("Enter item name: ").strip()

    if not item_name:
        print("Item name cannot be empty.")
        return

    # duplicate check
    for item in inventory:
        if item["item_name"].lower() == item_name.lower():
            print("Item already exists.")
            return

    try:
        quantity = int(input("Enter quantity: "))

        if quantity < 0:
            print("Quantity cannot be negative.")
            return

    except ValueError:
        print("Invalid number.")
        return

    item = {
        "item_id": generate_item_id(),
        "item_name": item_name,
        "quantity": quantity
    }

    inventory.append(item)
    save_inventory(inventory)

    print(f"{item_name} added successfully.")


# ---------------- VIEW + SEARCH + ACTION SYSTEM ----------------
def view_items():

    if not inventory:
        print("No inventory items found.")
        return

    print("\n===== INVENTORY =====")

    for index, item in enumerate(inventory, start=1):
        print(f"{index}. ID:{item['item_id']} | {item['item_name']} | Qty:{item['quantity']}")

    print("\nOptions:")
    print("1. Search Item")
    print("2. Back")

    choice = input("Enter choice: ")

    if choice == "1":
        search_items()

    else:
        return


# ---------------- SEARCH + ACTION  ----------------
def search_items():

    if not inventory:
        print("No inventory items found.")
        return

    search_name = input("Enter item name to search: ").strip()

    matches = find_item_by_name(search_name)

    if not matches:
        print("No matching item found.")
        return

    print("\nSearch Results:")

    for index, item in enumerate(matches, start=1):
        print(f"{index}. {item['item_name']} (Qty: {item['quantity']})")

    try:
        choice = int(input("\nSelect item number: "))

        if choice < 1 or choice > len(matches):
            print("Invalid choice.")
            return

    except ValueError:
        print("Invalid input.")
        return

    selected_item = matches[choice - 1]

    print(f"\nSelected: {selected_item['item_name']}")

    print("\n1. View")
    print("2. Update Quantity")
    print("3. Delete")
    print("4. Exit")

    action = input("Enter action: ")

   
    if action == "1":
        print(f"\nID: {selected_item['item_id']}")
        print(f"Item: {selected_item['item_name']}")
        print(f"Quantity: {selected_item['quantity']}")

    
    elif action == "2":
        try:
            new_qty = int(input("Enter new quantity: "))

            if new_qty < 0:
                print("Quantity cannot be negative.")
                return

        except ValueError:
            print("Invalid number.")
            return

        selected_item["quantity"] = new_qty
        save_inventory(inventory)

        print(f"{selected_item['item_name']} quantity updated successfully.")

   
    elif action == "3":
        confirm = input("Are you sure you want to delete this item? (y/n): ").lower()

        if confirm == "y":
            inventory.remove(selected_item)
            save_inventory(inventory)

            print(f"{selected_item['item_name']} deleted successfully.")
        else:
            print("Delete cancelled.")

    else:
        print("Exit.")