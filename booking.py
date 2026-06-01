from datetime import datetime
from customer import customers

from storage import (
    load_bookings,
    save_bookings
)

from inventory import (
    inventory,
    find_item_by_name
)

from customer import (
    get_or_create_customer
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
            "Invalid date format. Use YYYY-MM-DD."
        )

        return False

    if booking_start > booking_end:

        print(
            "Booking start date cannot be after booking end date."
        )

        return False

    if function_start > function_end:

        print(
            "Function start date cannot be after function end date."
        )

        return False

    if (
        function_start < booking_start
        or function_end > booking_end
    ):

        print(
            "Function dates must fall within booking dates."
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

        if "items" in booking:

            for item in booking["items"]:

                if item["item_id"] != item_id:
                    continue

                overlap = not (
                    booking_end
                    < booking["booking_start_date"]
                    or booking_start
                    > booking["booking_end_date"]
                )

                if overlap:
                    total_reserved += item["quantity"]

        else:
            # backward compatibility (old bookings)
            if booking["item_id"] == item_id:

                overlap = not (
                    booking_end
                    < booking["booking_start_date"]
                    or booking_start
                    > booking["booking_end_date"]
                )

                if overlap:
                    total_reserved += booking["quantity"]

    for item in inventory:

        if item["item_id"] == item_id:

            available = item["quantity"] - total_reserved

            return available >= required_quantity

    return False


#  STEP 1 + STEP 2 ADDITION
def add_multiple_items(
         booking_start,
         booking_end
):

    items = []

    while True:

        search_name = input(
            "Search item (or type 'done'): "
        ).strip()

        if search_name.lower() == "done":
            break

        matches = find_item_by_name(search_name)

        if not matches:
            print("No matching item found.")
            continue

        print("\nMatching Items:")

        for index, item in enumerate(matches, start=1):
            print(
                f"{index}. "
                f"{item['item_name']} "
                f"(Qty: {item['quantity']})"
            )

        try:
            choice = int(
                input("Select item number: ")
            )

            selected_item = matches[choice - 1]

            qty = int(
                input("Enter quantity: ")
            )

            if qty <= 0:
                print("Invalid quantity")
                continue

            if not check_availability(
                selected_item["item_id"],
                qty,
                booking_start,
                booking_end
            ):
                print(
                    "Not enough inventory available."
                )
                continue

            items.append({
                "item_id": selected_item["item_id"],
                "item_name": selected_item["item_name"],
                "quantity": qty
            })

            print("Item added successfully")

        except (
              ValueError,
              IndexError
                ):
            print("Invalid input")

    return items


def create_booking():

    

    customer_name = input(
        "Customer Name: "
    ).strip()

    #  STEP 2 ADDITION
    customer_phone = input(
        "Customer Phone (optional): "
    ).strip()

    customer = get_or_create_customer(
    customer_name,
    customer_phone
    )

    occasion = get_occasion()

    if occasion is None:
        return

    booking_start = input(
        "Booking Start Date (YYYY-MM-DD): "
    ).strip()

    booking_end = input(
        "Booking End Date (YYYY-MM-DD): "
    ).strip()

    function_start = input(
        "Function Start Date (YYYY-MM-DD): "
    ).strip()

    function_end = input(
        "Function End Date (YYYY-MM-DD): "
    ).strip()

    if not validate_dates(
        booking_start,
        booking_end,
        function_start,
        function_end
    ):
        return

    #  MULTI ITEM SELECTION (STEP 1)
    items = add_multiple_items( 
        booking_start,
        booking_end

    )

    if not items:
        print("No items selected for booking.")
        return

    try:
        total_amount = float(
            input("Total Amount: ")
        )

        advance_paid = float(
            input("Advance Paid: ")
        )

        if total_amount < 0 or advance_paid < 0:
            print("Invalid amount")
            return

    except ValueError:
        print("Invalid amount")
        return

    pending_amount = total_amount - advance_paid

    if pending_amount < 0:
        print("Advance cannot be greater than total amount")
        return

    payment_status = (
        "Paid"
        if pending_amount == 0
        else "Pending"
    )

    booking = {
        "booking_id": generate_booking_id(),
        "customer_id": customer["customer_id"],

        "occasion": occasion,
        "items": items,

        "booking_start_date": booking_start,
        "booking_end_date": booking_end,
        "function_start_date": function_start,
        "function_end_date": function_end,

        #  STEP 2 PAYMENT SYSTEM
        "payment": {
            "total_amount": total_amount,
            "advance_paid": advance_paid,
            "pending_amount": pending_amount,
            "status": payment_status
        },

        "delivery_status": "Pending",
        "return_status": "Pending",
        "booking_status": "Booked"
    }

    bookings.append(booking)
    save_bookings(bookings)

    print("Booking created successfully.")

def get_customer(customer_id):

    for customer in customers:

        if customer["customer_id"] == customer_id:
            return customer

    return None

def mark_delivered():

    booking_id = input(
        "Enter Booking ID: "
    )

    try:
        booking_id = int(booking_id)

    except ValueError:
        print("Invalid Booking ID.")
        return

    for booking in bookings:

        if booking["booking_id"] == booking_id:

            if booking["delivery_status"] == "Delivered":
                print("Already delivered.")
                return

            booking["delivery_status"] = "Delivered"
            booking["booking_status"] = "Delivered"

            save_bookings(bookings)

            print("Booking marked as delivered.")
            return

    print("Booking not found.")

def mark_returned():

    booking_id = input(
        "Enter Booking ID: "
    )

    try:
        booking_id = int(booking_id)

    except ValueError:
        print("Invalid Booking ID.")
        return

    for booking in bookings:

        if booking["booking_id"] == booking_id:

            if booking["return_status"] == "Returned":
                print("Already returned.")
                return

            booking["return_status"] = "Returned"
            booking["booking_status"] = "Completed"

            save_bookings(bookings)

            print("Booking marked as returned.")
            return

    print("Booking not found.")


def view_bookings():
    if not bookings:
        print("No bookings found.")
        return

    print("\n===== BOOKINGS =====")

    for booking in bookings:

        print(f"\nBooking ID: {booking.get('booking_id')}")

        # Resolve customer information (new and legacy formats)
        customer = None
        if "customer_id" in booking:
            customer = get_customer(booking["customer_id"])

        if customer:
            print(f"Customer: {customer.get('customer_name')}")
            if customer.get('customer_phone'):
                print(f"Phone: {customer.get('customer_phone')}")
        else:
            if "customer_name" in booking:
                print(f"Customer: {booking.get('customer_name')}")
            if "customer_phone" in booking:
                print(f"Phone: {booking.get('customer_phone')}")

        print("\nItems:")

        if "items" in booking:
            for item in booking["items"]:
                print(f" - {item['item_name']} | Qty: {item['quantity']}")
        else:
            print(f" - {booking.get('item_name')} | Qty: {booking.get('quantity')}")

        print(f"\nBooking Dates: {booking.get('booking_start_date')} to {booking.get('booking_end_date')}")
        print(f"Function Dates: {booking.get('function_start_date')} to {booking.get('function_end_date')}")

        # Payment and statuses
        if "payment" in booking:
            print("\nPayment Details:")
            print(f"Total: {booking['payment'].get('total_amount')}")
            print(f"Advance: {booking['payment'].get('advance_paid')}")
            print(f"Pending: {booking['payment'].get('pending_amount')}")
            print(f"Status: {booking['payment'].get('status')}")

        print(f"Delivery Status: {booking.get('delivery_status')}")
        print(f"Return Status: {booking.get('return_status')}")
        print(f"Booking Status: {booking.get('booking_status')}")

        print("-" * 40)