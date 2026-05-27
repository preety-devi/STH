from inventory import (
    add_item,
    view_items,
    search_items,
    update_quantity,
    delete_item
)


def main():

    while True:

        print("\n===== Sharma Tent House Inventory =====")

        print("1. Add Item")
        print("2. View Items")
        print("3. Search Item")
        print("4. Update Quantity")
        print("5. Delete Item")
        print("6. Exit")

        choice = input(
            "\nEnter your choice (1-6): "
        )

        if choice == "1":
            add_item()

        elif choice == "2":
            view_items()

        elif choice == "3":
            search_items()

        elif choice == "4":
            update_quantity()

        elif choice == "5":
            delete_item()

        elif choice == "6":
            print("Exiting program...")
            break

        else:
            print(
                "Invalid choice. "
                "Please enter a number from 1 to 6."
            )


if __name__ == "__main__":
    main()