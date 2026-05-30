import json
import os

FILE_NAME = "inventory.json"


def load_inventory():

    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return []


def save_inventory(inventory):

    with open(FILE_NAME, "w") as file:
        json.dump(inventory, file, indent=4)

BOOKING_FILE = "bookings.json"


def load_bookings():

    if not os.path.exists(BOOKING_FILE):
        return []

    try:
        with open(BOOKING_FILE, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return []


def save_bookings(bookings):

    with open(BOOKING_FILE, "w") as file:
        json.dump(bookings, file, indent=4)