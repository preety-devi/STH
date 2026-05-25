from inventory import add_item, view_items, update_quantity


while True:
    print("\n===== Sharma Tent House Inventory =====")
    print("1. Add Item")
    print("2. View Items")
    print("3. Update Quantity")
    print("4. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        add_item()

    elif choice == "2":
        view_items()

    elif choice == "3":
        update_quantity()

    elif choice == "4":
        print("Exiting program...")
        break

    else:
        print("Invalid choice. Please try again.")