from datetime import datetime

from storage import (
    load_bookings,
    save_bookings
)

from inventory import (
    inventory,
    find_item_by_name
)

bookings = load_bookings()


def generate_booking_id():

    if not bookings:
        return 1

    return max(
        booking["booking_id"]
        for booking in bookings
    ) + 1

def get_occasion():

    occasion = input(
        "Enter Occasion: "
    ).strip()

    if not occasion:

        print(
            "Occasion cannot be empty."
        )

        return None

    return occasion



def validate_dates(
    booking_start,
    booking_end,
    function_start,
    function_end
):

    try:

        booking_start = datetime.strptime(
            booking_start,
            "%Y-%m-%d"
        )

        booking_end = datetime.strptime(
            booking_end,
            "%Y-%m-%d"
        )

        function_start = datetime.strptime(
            function_start,
            "%Y-%m-%d"
        )

        function_end = datetime.strptime(
            function_end,
            "%Y-%m-%d"
        )

    except ValueError:

        print(
            "Invalid date format. "
            "Use YYYY-MM-DD."
        )

        return False

    if booking_start > booking_end:

        print(
            "Booking start date "
            "cannot be after booking end date."
        )

        return False

    if function_start > function_end:

        print(
            "Function start date "
            "cannot be after function end date."
        )

        return False

    if (
        function_start < booking_start
        or function_end > booking_end
    ):

        print(
            "Function dates must fall "
            "within booking dates."
        )

        return False

    return True


def check_availability(
    item_id,
    required_quantity,
    booking_start,
    booking_end
):

    total_reserved = 0

    for booking in bookings:

        if booking["item_id"] != item_id:
            continue

        overlap = not (
            booking_end
            < booking["booking_start_date"]
            or
            booking_start
            > booking["booking_end_date"]
        )

        if overlap:

            total_reserved += booking["quantity"]

    for item in inventory:

        if item["item_id"] == item_id:

            available = (
                item["quantity"]
                - total_reserved
            )

            return (
                available
                >= required_quantity
            )

    return False


def create_booking():

    search_name = input(
        "Search inventory item: "
    ).strip()

    matches = find_item_by_name(
        search_name
    )

    if not matches:

        print("No matching item found.")
        return

    print("\nMatching Items:")

    for index, item in enumerate(
        matches,
        start=1
    ):

        print(
            f"{index}. "
            f"{item['item_name']} "
            f"(Qty: {item['quantity']})"
        )

    try:

        choice = int(
            input(
                "\nSelect item number: "
            )
        )

        selected_item = matches[
            choice - 1
        ]

    except (
        ValueError,
        IndexError
    ):

        print("Invalid choice.")
        return

    customer_name = input(
        "Customer Name: "
    ).strip()

    occasion = get_occasion()

    if occasion is None:
     return

    booking_start = input(
        "Booking Start Date "
        "(YYYY-MM-DD): "
    ).strip()

    booking_end = input(
        "Booking End Date "
        "(YYYY-MM-DD): "
    ).strip()

    function_start = input(
        "Function Start Date "
        "(YYYY-MM-DD): "
    ).strip()

    function_end = input(
        "Function End Date "
        "(YYYY-MM-DD): "
    ).strip()

    if not validate_dates(
        booking_start,
        booking_end,
        function_start,
        function_end
    ):
        return

    try:

        quantity = int(
            input(
                "Quantity Required: "
            )
        )

        if quantity <= 0:

            print(
                "Quantity must be "
                "greater than zero."
            )

            return

    except ValueError:

        print("Invalid quantity.")
        return

    if not check_availability(
        selected_item["item_id"],
        quantity,
        booking_start,
        booking_end
    ):

        print(
            "Booking rejected. "
            "Not enough inventory available."
        )

        return

    booking = {
        "booking_id": generate_booking_id(),
        "customer_name": customer_name,
        "occasion": occasion,
        "item_id": selected_item["item_id"],
        "item_name": selected_item["item_name"],
        "quantity": quantity,
        "booking_start_date": booking_start,
        "booking_end_date": booking_end,
        "function_start_date": function_start,
        "function_end_date": function_end
    }

    bookings.append(booking)

    save_bookings(bookings)

    print(
        "Booking created successfully."
    )


def view_bookings():

    if not bookings:

        print("No bookings found.")
        return

    print("\n===== BOOKINGS =====")

    for booking in bookings:

        print(
            f"\nBooking ID: "
            f"{booking['booking_id']}"
        )

        print(
            f"Customer: "
            f"{booking['customer_name']}"
        )

        print(
            f"Occasion: "
            f"{booking['occasion']}"
        )

        print(
            f"Item: "
            f"{booking['item_name']}"
        )

        print(
            f"Quantity: "
            f"{booking['quantity']}"
        )

        print(
            f"Booking Dates: "
            f"{booking['booking_start_date']} "
            f"to "
            f"{booking['booking_end_date']}"
        )

        print(
            f"Function Dates: "
            f"{booking['function_start_date']} "
            f"to "
            f"{booking['function_end_date']}"
        )

        print("-" * 30)