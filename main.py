from inventory import (
    add_item,
    view_items
)

from booking import (
    create_booking,
    view_bookings,
    mark_delivered,
    mark_returned
)


def main():

    while True:

        print("\n===== Sharma Tent House =====")

        print("1. Add Inventory Item")
        print("2. View Inventory")
        print("3. Create Booking")
        print("4. View Bookings")
        print("5. Mark Delivered")
        print("6. Mark Returned")
        print("7. Exit")

        choice = input(
            "\nEnter your choice (1-7): "
        )

        if choice == "1":
            add_item()

        elif choice == "2":
            view_items()

        elif choice == "3":
            create_booking()

        elif choice == "4":
            view_bookings()

        elif choice == "5":
          mark_delivered()

        elif choice == "6":
          mark_returned()

        elif choice == "7":
          print("Exiting program...")
          break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()