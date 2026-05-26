from inventory import (
    add_item,
    view_items,
    update_quantity,
    delete_item
)


def main():

    while True:

        print("\n===== Sharma Tent House Inventory =====")

        print("1. Add Item")
        print("2. View Items")
        print("3. Update Quantity")
        print("4. Delete Item")
        print("5. Exit")

        choice = input(
            "\nEnter your choice (1-5): "
        )

        if choice == "1":
            add_item()

        elif choice == "2":
            view_items()

        elif choice == "3":
            update_quantity()

        elif choice == "4":
            delete_item()

        elif choice == "5":
            print("Exiting program...")
            break

        else:
            print(
                "Invalid choice. "
                "Please enter a number from 1 to 5."
            )


if __name__ == "__main__":
    main()