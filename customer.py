from storage import (
    load_customers,
    save_customers
)

customers = load_customers()

def view_customers():

    if not customers:

        print("No customers found.")
        return

    print("\n===== CUSTOMERS =====")

    for customer in customers:

        print(
            f"{customer['customer_id']} | "
            f"{customer['customer_name']} | "
            f"{customer['customer_phone']}"
        )

def generate_customer_id():

    if not customers:
        return 1

    return max(
        customer["customer_id"]
        for customer in customers
    ) + 1


def get_or_create_customer(
    customer_name,
    customer_phone
):

    for customer in customers:

        if (
            customer["customer_name"].lower()
            == customer_name.lower()
            and
            customer["customer_phone"]
            == customer_phone
        ):

            return customer

    customer = {
        "customer_id": generate_customer_id(),
        "customer_name": customer_name,
        "customer_phone": customer_phone
    }

    customers.append(customer)

    save_customers(customers)

    return customer