1 Three-Sentence Specification

This program helps Sharma Tent House manage bookings, rented items, payments, deliveries, returns, and damaged items using a command-line Python application.

The main users are Rakesh (Owner) and Ankit(Operator). Rakesh ji will mainly check bookings, item availability, and payments, while Ankit can enter new bookings, update deliveries, and manage returns.

The project will be considered complete if the system can safely store data in JSON files, prevent double-booking of items, track payments and damages, and work correctly after restarting the program.

2 Information The Program Must Remember

A.Customer
| Field       | Type   | Required |
| ----------- | ------ | -------- |
| customer_id | string | Yes      |
| name        | string | Yes      |
| phone       | string | Yes      |
| address     | string | Optional |
| notes       | string | Optional |




B. Inventory Items

| Field              | Type    | Required |
| ------------------ | ------- | -------- |
| item_id            | string  | Yes      |
| item_name          | string  | Yes      |
| category           | string  | Yes      |
| total_quantity     | integer | Yes      |
| available_quantity | integer | Yes      |
| rent_per_day       | float   | Yes      |
| damage_charge      | float   | Yes      |
| unique_item        | boolean | Yes      |
| status             | string  | Yes      |

Example Categories
Chairs
Tables
Fans
Sound System
Sofa
Dinner Set

Some items are unique (sound system), while some are bulk items (chairs).

C. Bookings
| Field          | Type   | Required |
| -------------- | ------ | -------- |
| booking_id     | string | Yes      |
| customer_id    | string | Yes      |
| event_name     | string | Yes      |
| event_address  | string | Yes      |
| start_date     | string | Yes      |
| end_date       | string | Yes      |
| booking_status | string | Yes      |
| total_amount   | float  | Yes      |
| deposit_paid   | float  | Yes      |
| balance_due    | float  | Yes      |
| created_date   | string | Yes      |



Every booking needs dates because item availability depends on dates.

D. Booking Items
| Field           | Type    | Required |
| --------------- | ------- | -------- |
| booking_item_id | string  | Yes      |
| booking_id      | string  | Yes      |
| item_id         | string  | Yes      |
| quantity        | integer | Yes      |
| price_per_day   | float   | Yes      |
| total_price     | float   | Yes      |


One booking contains many items.

E. Payments
| Field        | Type   | Required |
| ------------ | ------ | -------- |
| payment_id   | string | Yes      |
| booking_id   | string | Yes      |
| amount       | float  | Yes      |
| payment_type | string | Yes      |
| payment_date | string | Yes      |

Payment Types
-Deposit
-Full Payment
-Refund
-Damage Deduction

F. Deliveries & Returns
| Field         | Type    | Required |
| ------------- | ------- | -------- |
| delivery_id   | string  | Yes      |
| booking_id    | string  | Yes      |
| delivery_date | string  | Yes      |
| return_date   | string  | Optional |
| returned      | boolean | Yes      |
| notes         | string  | Optional |



G. Damage Records

| Field            | Type    | Required |
| ---------------- | ------- | -------- |
| damage_id        | string  | Yes      |
| booking_id       | string  | Yes      |
| item_id          | string  | Yes      |
| quantity_damaged | integer | Yes      |
| damage_type      | string  | Yes      |
| extra_charge     | float   | Yes      |

Damage Types
-Missing
-Broken
-Scratched
-Late Return



 3 How The Groupings Connect To Each Other

Customers create bookings.

Each booking can contain many booking items.

Booking items connect bookings with inventory items.

Payments are connected to bookings because customers may pay multiple times.

Damage records are connected to bookings and inventory items.

Unique item units are connected to inventory items so the program knows exactly which expensive item is out at an event.

When a booking is confirmed, inventory quantities reduce temporarily. When items return, quantities increase again.


File Structure

I will use multiple JSON files because it keeps data cleaner and easier to manage.

##customers.json
[
  {
    "customer_id": "C001",
    "name": "Rajesh Agarwal",
    "phone": "9876543210",
    "address": "Talwandi, Kota",
    "notes": "Regular customer"
  }
]
##inventory.json
[
  {
    "item_id": "I001",
    "item_name": "White Plastic Chair",
    "category": "Chair",
    "total_quantity": 500,
    "available_quantity": 320,
    "rent_per_day": 12,
    "damage_charge": 250,
    "unique_item": false,
    "status": "Available"
  }
]
##bookings.json
[
  {
    "booking_id": "B001",
    "customer_id": "C001",
    "event_name": "Agarwal Wedding",
    "event_address": "Mahaveer Nagar, Kota",
    "start_date": "2026-12-18",
    "end_date": "2026-12-20",
    "booking_status": "Confirmed",
    "total_amount": 45000,
    "deposit_paid": 10000,
    "balance_due": 35000,
    "created_date": "2026-05-20"
  }
]
##booking_items.json
[
  {
    "booking_item_id": "BI001",
    "booking_id": "B001",
    "item_id": "I001",
    "quantity": 200,
    "price_per_day": 12,
    "total_price": 4800
  }
]
##payments.json
[
  {
    "payment_id": "P001",
    "booking_id": "B001",
    "amount": 10000,
    "payment_type": "Deposit",
    "payment_date": "2026-05-20"
  }
]
##damages.json
[
  {
    "damage_id": "D001",
    "booking_id": "B001",
    "item_id": "I001",
    "quantity_damaged": 2,
    "damage_type": "Broken",
    "extra_charge": 500
  }
]
Multiple Files Beacuse: 
Easier to read
Easier to debug
Safer if one file becomes corrupted
Problem When Business Grows

If there are 5000 bookings per year, searching JSON files may become slow. A database may be needed later.



5 Operations

User adds a new customer. The system saves customer details and shows the customer ID.

User adds inventory items. The system stores item details and quantity.
Example: Ankit adds 500 white chairs and 30 round tables into inventory.

User checks item availability for specific dates. The system checks existing bookings and shows available quantity.
Example: Customer asks for 250 chairs on 18 December, and system shows only 220 are free.

User creates a booking. The system verifies item availability, saves the booking, and calculates total amount.
Example: Booking includes 200 chairs, 4 fans, and 2 gas burners for a wedding.

User adds multiple items in one booking. The system calculates total cost for all items.
Example: One booking contains chairs, tables, fans, sofa set, and shamiana.

User records advance payment or deposit. The system updates remaining balance.
Example: Customer pays ₹10,000 deposit for a ₹45,000 booking.

User views all current bookings. The system displays active and upcoming bookings.
Example: Rakesh ji checks all bookings for next week.

User searches booking by customer name or phone number. The system shows matching bookings.
Example: Searching “Agarwal” shows all related bookings.

User edits booking details. The system updates prices, quantities, and totals.
Example: Customer increases chairs from 200 to 250.

User cancels a booking. The system restores item availability.
Example: Customer postpones wedding and booking gets cancelled.

User marks items as delivered. The system changes item status to “Out for Rent.”
Example: Chairs and tables are sent to a farmhouse event.

User checks which items are currently out for rent. The system shows event details and return dates.
Example: System shows pedestal fans are at a booking in Mahaveer Nagar.

User records returned items. The system updates inventory quantities.
Example: After the event, 198 chairs are returned successfully.

User reports damaged items. The system adds damage charges to customer balance.
Example: Two plates are broken during the function.

User reports missing items. The system deducts charges from deposit.
Example: One pedestal fan is missing after collection.

User checks pending payments. The system shows customers who still owe money.
Example: Customer still has ₹8,000 remaining after event completion.

User views damage and loss reports. The system shows total losses and damaged items.
Example: System displays total damage cost for last month.
   
User closes the program. The system automatically saves all data in JSON files.
Example: Next morning all bookings and records are still available.




6  Things That Can Go Wrong

(a)JSON file missing on first run.
System creates a new empty file automatically.

(b)  Invalid date entered.
System rejects input and asks again.

(c)  Customer phone number entered incorrectly.
System validates number length.

(d)  User tries booking more chairs than available.
System blocks booking.

(e) User enters negative quantity.
System rejects value.

(f) Customer cancels after partial payment.
System marks refund or pending adjustment.

(g) Items returned late.
System adds late charges.

(h) Returned quantity exceeds booked quantity.
System blocks entry.

(i) Duplicate customer accidentally created.
System warns if same phone number exists.

(j) Program closes unexpectedly during save.
System uses temporary save file before replacing original file.

(k) User tries to close booking with missing items.
System refuses until issue resolved.

(l)  Damaged items exceed deposit value.
System marks extra amount due.

(m) Unique item already booked elsewhere.
System blocks second booking.

(n) Inventory file becomes corrupted.
System creates backup recovery option.

(o) Booking dates overlap incorrectly.
System checks all active bookings before confirming.



7 One Thing I Don’t Know Yet

I am not fully sure about the best way to check item availability when multiple bookings have overlapping dates.
I am unsure how to properly update inventory quantities when items are damaged, missing, or returned late
I am unsure how to design a simple but user-friendly command-line menu system