from datetime import datetime
from decimal import Decimal
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
    occasion_start,
    occasion_end
):

    try:

        booking_start = datetime.strptime(
            booking_start,
            "%Y-%m-%d %I:%M %p"
        )

        booking_end = datetime.strptime(
            booking_end,
            "%Y-%m-%d %I:%M %p"
        )

        occasion_start = datetime.strptime(
            occasion_start,
            "%Y-%m-%d"
        ).date()

        occasion_end = datetime.strptime(
            occasion_end,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        print(
            "Invalid format. Use YYYY-MM-DD HH:MM AM/PM."
        )

        return False

    if booking_start > booking_end:

        print(
            "Booking start date cannot be after booking end date."
        )

        return False

    if occasion_start > occasion_end:

        print(
            "Occasion start date cannot be after occasion end date."
        )

        return False

    if (
        occasion_start < booking_start.date()
        or occasion_end > booking_end.date()
    ):

        print(
            "Occasion dates must fall within booking dates."
        )

        return False

    return True


def get_datetime_input(prompt):

    while True:

        date_value = input(prompt).strip()

        try:
            datetime.strptime(
                date_value,
                "%Y-%m-%d %I:%M %p"
            )
            return date_value

        except ValueError:
            print(
                "Invalid date. Enter again."
            )


def get_date_input(prompt):

    while True:

        date_value = input(prompt).strip()

        try:
            datetime.strptime(
                date_value,
                "%Y-%m-%d"
            )
            return date_value

        except ValueError:
            print(
                "Invalid date. Enter again."
            )


def get_valid_phone(prompt):

    while True:

        phone = input(prompt).strip()

        if not phone.isdigit() or len(phone) != 10:
            print(
                "Invalid phone number. Please enter again."
            )
            continue

        return phone


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



def get_available_quantity(
    item_id,
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

    for item in inventory:

        if item["item_id"] == item_id:

            return (
                item["quantity"]
                - total_reserved
            )

    return 0


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
            available_qty = get_available_quantity(
                item["item_id"],
                booking_start,
                booking_end
            )
            print(
                f"{index}. "
                f"{item['item_name']} "
                f"(Available: {available_qty}) "
                f"(Rate: {item['rent_price']})"
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
                print("Not enough inventory available.")
                continue

            items.append({
                "item_id": selected_item["item_id"],
                "item_name": selected_item["item_name"],
                "quantity": qty,
                "rent_price": selected_item.get("rent_price")
            })
            print("Item added successfully")

        except (
            ValueError,
            IndexError
        ):
            print("Invalid input")

    return items

               

        
        

def select_customer():

    while True:

        print("\n1. Use Existing Customer")
        print("2. Create New Customer")

        choice = input(
            "Enter choice: "
        ).strip()

        if choice == "1":

            if not customers:

                print(
                    "No customers found."
                )

                return None

            print("\n===== CUSTOMERS =====")

            for customer in customers:

                print(
                    f"{customer['customer_id']} | "
                    f"{customer['customer_name']} | "
                    f"{customer['customer_phone']}"
                )

            while True:

                try:

                    customer_id = int(
                        input(
                            "Enter Customer ID: "
                        )
                    )
                    break

                except ValueError:

                    print(
                        "Invalid Customer ID. Please enter again."
                    )

            for customer in customers:

                if (
                    customer["customer_id"]
                    == customer_id
                ):
                    return customer

            print("Customer not found.")
            return None

        elif choice == "2":

            customer_name = input(
                "Customer Name: "
            ).strip()

            while not customer_name:
                print(
                    "Customer name cannot be empty. Please enter again."
                )
                customer_name = input(
                    "Customer Name: "
                ).strip()

            customer_phone = get_valid_phone(
                "Customer Phone: "
            )

            existing_customer = next(
                (
                    customer for customer in customers
                    if customer["customer_phone"] == customer_phone
                ),
                None
            )

            if existing_customer:
                print(
                    "Customer already exists. Using existing customer."
                )
                return existing_customer

            return get_or_create_customer(
                customer_name,
                customer_phone
            )

        else:

            print("Invalid choice. Please enter again.")


def create_booking():

    customer = select_customer()

    if customer is None:
       return

    occasion = get_occasion()

    if occasion is None:
        return

    booking_start = get_datetime_input(
        "Booking Start Date (YYYY-MM-DD HH:MM AM/PM): "
    )

    booking_end = get_datetime_input(
        "Booking End Date (YYYY-MM-DD HH:MM AM/PM): "
    )

    occasion_start = get_date_input(
        "Occasion Start Date (YYYY-MM-DD): "
    )

    occasion_end = get_date_input(
        "Occasion End Date (YYYY-MM-DD): "
    )

    while not validate_dates(
        booking_start,
        booking_end,
        occasion_start,
        occasion_end
    ):
        print(
            "Invalid date. Enter again."
        )

        booking_start = get_datetime_input(
            "Booking Start Date (YYYY-MM-DD HH:MM AM/PM): "
        )

        booking_end = get_datetime_input(
            "Booking End Date (YYYY-MM-DD HH:MM AM/PM): "
        )

        occasion_start = get_date_input(
            "Occasion Start Date (YYYY-MM-DD): "
        )

        occasion_end = get_date_input(
            "Occasion End Date (YYYY-MM-DD): "
        )

    items = add_multiple_items(
        booking_start,
        booking_end
    )

    if not items:
        print(
            "No items selected for booking."
        )
        return

    total_amount = Decimal("0")

    for item in items:

        item_total = (
            Decimal(str(item["quantity"]))
            * Decimal(item["rent_price"])
        )

        total_amount += item_total

    print("\n===== BOOKING SUMMARY =====")

    for item in items:

        item_total = (
            Decimal(str(item["quantity"]))
            * Decimal(item["rent_price"])
        )

        print(
            f"{item['item_name']} | "
            f"Qty: {item['quantity']} | "
            f"Rate: {item['rent_price']} | "
            f"Amount: {item_total}"
        )

    print(f"\nTotal Amount: {total_amount}")

    while True:

        try:
            discount = Decimal(
                input("Discount: ")
            )

            if discount < 0:
                print("Invalid discount. Enter again.")
                continue

            if discount > total_amount:
                print(
                    "Discount cannot be greater than total amount."
                )
                continue

            break

        except Exception:
            print("Invalid discount. Enter again.")

    final_amount = (
        total_amount - discount
    )

    print(
        f"Final Amount: {final_amount}"
    )

    while True:

        try:
            advance_paid = Decimal(
                input("Advance Paid: ")
            )

            if advance_paid < 0:
                print("Invalid amount. Enter again.")
                continue

            if advance_paid > final_amount:
                print(
                    "Advance cannot be greater than total amount. Enter again."
                )
                continue

            break

        except Exception:
            print("Invalid amount. Enter again.")

    pending_amount = (
        final_amount - advance_paid
    )

    if pending_amount < 0:

        print(
            "Advance cannot be greater "
            "than total amount."
        )

        return

    payment_status = (
        "Paid"
        if pending_amount == 0
        else "Pending"
    )

    confirm = input(
        "\nConfirm Booking? (y/n): "
    ).lower()

    if confirm != "y":

        print("Booking cancelled.")
        return

    booking = {
        "booking_id": generate_booking_id(),
        "customer_id": customer["customer_id"],

        "occasion": occasion,
        "items": items,

        "booking_start_date": booking_start,
        "booking_end_date": booking_end,
        "occasion_start_date": occasion_start,
        "occasion_end_date": occasion_end,

        "payment": {
            "total_amount": str(final_amount),
            "advance_paid": str(advance_paid),
            "pending_amount": str(pending_amount),
            "status": payment_status
        },

        "delivery_status": "Pending",
        "return_status": "Pending",
        "booking_status": "Booked"
    }

    bookings.append(booking)

    save_bookings(bookings)

    print(
        "Booking created successfully."
    )

def get_customer(customer_id):

    for customer in customers:

        if customer["customer_id"] == customer_id:
            return customer

    return None

def show_booking_list():

    if not bookings:
        print("No bookings found.")
        return

    print("\n===== BOOKING LIST =====")

    for booking in bookings:

        customer = get_customer(
            booking["customer_id"]
        )

        if customer:

            print(
                f"ID: {booking['booking_id']} | "
                f"{customer['customer_name']} | "
                f"{customer['customer_phone']}"
            )

def mark_delivered():
    show_booking_list()

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
    show_booking_list()

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

            if booking["delivery_status"] != "Delivered":

                print(
                    "Booking must be delivered first."
                )

                return

            if booking["return_status"] == "Returned":

                print("Already returned.")
                return

            damage = input(
                "Any damaged items? (y/n): "
            ).lower()

            if damage == "y":

                if "damaged_items" not in booking:
                    booking["damaged_items"] = []

                item_name = input(
                    "Damaged Item Name: "
                ).strip()

                try:

                    qty = int(
                        input(
                            "Damaged Quantity: "
                        )
                    )

                except ValueError:

                    print(
                        "Invalid quantity."
                    )

                    return

                reason = input(
                    "Reason: "
                ).strip()

                booking["damaged_items"].append(
                    {
                        "item_name": item_name,
                        "quantity": qty,
                        "reason": reason
                    }
                )

            booking["return_status"] = "Returned"

            booking["booking_status"] = "Completed"

            save_bookings(bookings)

            print(
                "Booking marked as returned."
            )

            return

    print("Booking not found.")

from decimal import Decimal


def update_payment():
    show_booking_list()

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

            if "payment" not in booking:

                print(
                    "No payment information found."
                )

                return

            pending_amount = Decimal(
                str(
                    booking["payment"][
                        "pending_amount"
                    ]
                )
            )

            advance_paid = Decimal(
                str(
                    booking["payment"][
                        "advance_paid"
                    ]
                )
            )

            print(
                f"Current Pending Amount: "
                f"{pending_amount}"
            )

            try:

                amount_received = Decimal(
                    input(
                        "Enter Amount Received: "
                    )
                )

                if amount_received <= 0:

                    print(
                        "Amount must be greater "
                        "than zero."
                    )

                    return

            except:

                print("Invalid amount.")
                return

            if amount_received > pending_amount:

                print(
                    "Amount cannot be greater "
                    "than pending amount."
                )

                return

            advance_paid += amount_received

            pending_amount -= amount_received

            booking["payment"][
                "advance_paid"
            ] = str(
                advance_paid
            )

            booking["payment"][
                "pending_amount"
            ] = str(
                pending_amount
            )

            if pending_amount == Decimal("0"):

                booking["payment"][
                    "status"
                ] = "Paid"

            else:

                booking["payment"][
                    "status"
                ] = "Pending"

            save_bookings(bookings)

            print(
                "Payment updated successfully."
            )

            print(
                f"Remaining Pending Amount: "
                f"{pending_amount}"
            )

            print(
                f"Payment Status: "
                f"{booking['payment']['status']}"
            )

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

             print(
                 f" - {item['item_name']} | "
                 f"Qty: {item['quantity']} | "
                 f"Rate: {item.get('rent_price', 'N/A')}"
              )

        
        else:
            print(f" - {booking.get('item_name')} | Qty: {booking.get('quantity')}")

        print(f"\nBooking Dates: {booking.get('booking_start_date')} to {booking.get('booking_end_date')}")
        print(f"Occasion Dates: {booking.get('occasion_start_date')} to {booking.get('occasion_end_date')}")

        # Payment and statuses
        if "payment" in booking:
            print("\nPayment Details:")
            print(f"Total: {booking['payment'].get('total_amount')}")
            print(f"Advance: {booking['payment'].get('advance_paid')}")
            print(f"Pending: {booking['payment'].get('pending_amount')}")
            print(f"Status: {booking['payment'].get('status')}")

        if "damaged_items" in booking:

          print("\nDamaged Items:")

          for item in booking["damaged_items"]:

           print(
              f"{item['item_name']} | "
              f"Qty: {item['quantity']} | "
              f"Reason: {item['reason']}"
            )

        print(f"Delivery Status: {booking.get('delivery_status')}")
        print(f"Return Status: {booking.get('return_status')}")
        print(f"Booking Status: {booking.get('booking_status')}")

        print("-" * 40)

