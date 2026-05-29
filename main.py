from inventory import (
    add_item,
    view_items,
    search_items
)

def main():

    while True:

        print("\n===== Sharma Tent House Inventory =====")

        print("1. Add Item")
        print("2. View / Search Items")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")

        if choice == "1":
            add_item()

        elif choice == "2":
            view_items()   # This will also allow searching and actions on items

        elif choice == "3":
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please enter 1-3.")


if __name__ == "__main__":
    main()