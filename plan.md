1. Three-Sentence Specification

This program helps Sharma Tent House manage bookings, rented items, payments, deliveries, returns, and damaged items using a command-line Python application.

The main users are Rakesh (Owner) and Ankit(Operator). Rakesh ji will mainly check bookings, item availability, and payments, while Ankit can enter new bookings, update deliveries, and manage returns.

The project will be considered complete if the system can safely store data in JSON files, prevent double-booking of items, track payments and damages, and work correctly after restarting the program.


2. Information The Program Must Remember

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
| rent_per_day       | float   | Yes      |
| damage_charge      | float   | Yes      |
| item_type          | string  | Yes      |

Item Type Values
Bulk
Unique

Example Categories
Chairs
Tables
Fans
Sound System
Sofa
Dinner Set


Availability will not be permanently stored because it depends on booking dates.

The system will calculate available quantity using existing bookings and overlapping dates.


C. Unique Item Units

This table is only for expensive individually trackable items.

| Field     | Type   | Required |
| --------- | ------ | -------- |
| unit_id   | string | Yes      |
| item_id   | string | Yes      |
| unit_name | string | Yes      |

Example

| unit_id | item_id | unit_name      |
| ------- | ------- | -------------- |
| U001    | I010    | Sound System A |
| U002    | I010    | Sound System B |

This helps the system know exactly which unique item is booked.

D. Bookings

| Field            | Type   | Required |
| ---------------- | ------ | -------- |
| booking_id       | string | Yes      |
| customer_id      | string | Yes      |
| event_name       | string | Yes      |
| event_address    | string | Yes      |
| event_start_date | string | Yes      |
| event_end_date   | string | Yes      |
| booking_status   | string | Yes      |
| total_amount     | float  | Yes      |
| created_date     | string | Yes      |

Booking Status Values :
Pending
Confirmed
Cancelled
Completed

Event dates represent the actual function dates.
Item availability will not be checked using event dates directly because items may leave before the event and return after the event.
Availability checking will use delivery and expected return dates from the Deliveries & Returns records.

Remaining balance will be calculated using total amount and payment records. 
Every booking needs dates because item availability depends on dates.

E. Booking Items

| Field             | Type    | Required |
| ----------------- | ------- | -------- |
| booking_item_id   | string  | Yes      |
| unit_id           | string  | Optional |
| quantity_booked   | integer | Yes      |
| quantity_sent     | integer | Yes      |
| quantity_returned | integer | Yes      |
| price_per_day     | float   | Yes      |
| discount_amount   | float   | Optional |
| total_price       | float   | Yes      |

One booking contains many items.
Returned quantity is stored per booking item so partial returns can be tracked.
For bulk items unit_id will stay empty, but for unique items the booking item will store the exact unit being rented.
Example:
Booking Item:
item_id = Sound System
unit_id = U001
means Sound System A is booked.



F. Payments

| Field        | Type   | Required |
| ------------ | ------ | -------- |
| payment_id   | string | Yes      |
| booking_id   | string | Yes      |
| amount       | float  | Yes      |
| payment_type | string | Yes      |
| payment_date | string | Yes      |

Payment Types :
Deposit
Partial Payment
Full Payment
Refund
Damage Charge

G. Deliveries & Returns

| Field                | Type   | Required |
| -------------        | ------ | -------- |
| delivery_id          | string | Yes      |
| booking_id           | string | Yes      |
| delivery_date        | string | Yes      |
| expected_return_date | string | Yes      |
| actual_return_date   | string | Optional |
| status               | string | Yes      |
| notes                | string | Optional |

Status Values :
Pending
Delivered
Partially Returned
Returned


H. Damage Records

| Field            | Type    | Required |
| ---------------- | ------- | -------- |
| damage_id        | string  | Yes      |
| booking_id       | string  | Yes      |
| item_id          | string  | Yes      |
| damage_type      | string  | Yes      |
| quantity_damaged | integer | Yes      |
| extra_charge     | float   | Yes      |


Damage Types:
Broken
Scratched

Missing items and late returns are stored separately because they affect billing and inventory differently.

I. Missing Item Records

| Field            | Type     | Required |
|------------------|----------|----------|
| missing_id       | string   | Yes      |
| booking_item_id  | string   | Yes      |
| quantity_missing | integer  | Yes      |
| missing_charge   | float    | Yes      |

J. Late Return Records

| Field           | Type    | Required |
|-----------------|---------|----------|
| late_return_id  | string  | Yes      |
| booking_item_id | string  | Yes      |
| delayed_days    | integer | Yes      |
| late_fee        | float   | Yes      |



3. How The Groupings Connect To Each Other

Customers create bookings.

Each booking can contain many booking items.

Booking items connect bookings with inventory items.

Payments are connected to bookings because customers may pay multiple times.

Damage records are connected to bookings and inventory items.

Unique item units are connected to inventory items so the program knows exactly which expensive item is booked.

Availability is calculated using:
delivery dates
expected return dates
existing bookings
overlapping schedules

When items are returned, returned quantity is updated.


4. File Structure

I will use multiple JSON files because it keeps data cleaner and easier to manage.

customers.json
inventory.json
unique_units.json
bookings.json
booking_items.json
payments.json
deliveries.json
damages.json
missing_items.json
late_returns.json

Examples -

customers.json

[
  {
    "customer_id": "C001",
    "name": "Parkash Sharma",
    "phone": "9876543XXXX",
    "address": "Talwandi, Kota",
    "notes": "Regular customer"
  }
]

bookings.json

[
  {
    "booking_id": "B001",
    "customer_id": "C001",
    "event_name": "Sharma Wedding",
    "event_address": "Mahaveer Nagar, Kota",
    "event_start_date": "2026-12-18",
    "event_end_date": "2026-12-19",
    "booking_status": "Confirmed",
    "total_amount": 45000,
    "created_date": "2026-11-01"
  }
]

booking_items.json

[
  {
    "booking_item_id": "BI001",
    "booking_id": "B001",
    "item_id": "I001",
    "unit_id": null,
    "quantity_booked": 200,
    "quantity_sent": 200,
    "quantity_returned": 198,
    "price_per_day": 10,
    "discount_amount": 200,
    "total_price": 3800
  },
  {
    "booking_item_id": "BI002",
    "booking_id": "B001",
    "item_id": "I010",
    "unit_id": "U001",
    "quantity_booked": 1,
    "quantity_sent": 1,
    "quantity_returned": 1,
    "price_per_day": 5000,
    "discount_amount": 0,
    "total_price": 5000
  }
]

payments.json
[
  {
    "payment_id": "P001",
    "booking_id": "B001",
    "amount": 10000,
    "payment_type": "Deposit",
    "payment_date": "2026-12-10"
  }
]



Why Multiple Files
Easier to read
Easier to debug
Easier to manage separately
Safer if one file becomes corrupted

Problem When Business Grows

If there are thousands of bookings, searching JSON files may become slower. A database may be needed later.


5. Operations

(a) User adds a new customer.
The system stores customer details and generates customer ID.

Example:
Ankit adds customer “Rajesh Agarwal” with phone number and address.

(b) User adds inventory items.
The system stores item details and quantity.

Example:
Ankit adds:

500 white chairs
30 round tables
12 pedestal fans

(c) User adds unique item units for expensive items.
Example:
The system stores:
Sound System A
Sound System B
so both can be tracked separately.

(d) User checks item availability for specific dates.
The system checks overlapping bookings before showing available quantity.
Example:
A customer asks for 250 chairs on 18 December and the system shows only 220 are available.

(e) User creates a booking.
The system verifies availability and stores booking details.
Example:
Booking includes:

200 chairs
10 tables
4 fans
for a wedding event.

(f) User adds multiple items in one booking.
The system calculates total cost for all items together.
Example:
One booking contains chairs, tables, sofa sets, fans, and shamiana items.

(g) User records deposit or payment.
The system stores payment records and calculates remaining amount whenever needed.
Example:
Customer pays ₹10,000 as advance payment for a ₹45,000 booking.

(h) User views all current and upcoming bookings.
The system shows active and future events.
Example:
Rakesh ji checks all bookings for next week.

(i) User searches bookings using customer name or phone number.
Example:
Searching “Agarwal” shows all related bookings.

(j) User edits booking quantities or dates.
The system rechecks availability before saving changes.
Example:
Customer increases chair quantity from 200 to 250.

(k) User cancels a booking.
The system removes that booking from availability calculations.
Example:
Customer postpones wedding and booking gets cancelled.

(l) User marks items as delivered.
The system updates delivery status.
Example:
Chairs and tables are sent to a farmhouse event.

(m) User checks which items are currently out for rent.
Example:
System shows pedestal fans are currently booked for an event in Mahaveer Nagar.

(n) User records returned quantities.
The system updates returned quantity for booking items.
Example:
Out of 200 chairs, only 198 are returned.

(o) User reports damaged items.
The system stores damage details and extra charges.
Example:
Two dinner plates are reported broken after the event.

(p) User reports missing items.
The system records missing quantity and charges.
Example:
One pedestal fan is missing after collection.

(q) User records late return charges.
The system adds late fees to the booking.
Example:
Customer returns tables 2 days late.

(r) User checks pending payments.
The system shows customers who still owe money.
Example:
Customer still has ₹8,000 remaining after the event.

(s) User views damage and loss reports.
Example:
System displays total damaged and missing items for the last month.

(t) User closes the program.
The system automatically saves all JSON data safely.
Example:
After restarting next morning, all bookings and inventory records are still available.

(u) User checks idle inventory items.
The system shows items that were rarely booked in a selected time period.
Example:
System shows that decorative sofa sets were booked only once last month.

(v) User checks daily activity schedule.
The system shows deliveries, returns, and active bookings for a selected date.
Example:
Rakesh ji checks all deliveries and pickups happening on 22 December.

6. Things That Can Go Wrong
(a) JSON file missing on first run.
    System creates empty file automatically.

(b) Invalid date entered.
   System rejects input.

(c) Customer phone number entered incorrectly.
   System validates number length.

(d) User tries booking more items than available.
   System blocks booking.

(e) Negative quantity entered.
   System rejects value.

(f) Customer cancels after partial payment.
   System records refund adjustment.

(g) Items returned late.
   System adds late charges.

(h) Returned quantity exceeds booked quantity.
   System blocks entry.

(i) Duplicate customer accidentally created.
   System warns if same phone number exists.

(j) Program closes unexpectedly during save.
   System uses temporary save file before replacing original file.

(k) Damage charges exceed deposit amount.
   System shows extra pending amount.

(l) Same unique item booked for overlapping dates.
   System blocks booking.

(m) Booking dates overlap incorrectly.
   System checks all active bookings before confirming.


7. One Thing I Don’t Know Yet

I am not fully sure about the best way to calculate item availability efficiently when many bookings overlap on different dates.

I am still unsure about the best way to design a simple but user-friendly command-line menu system.

I may later move from JSON files to a database if the amount of data becomes very large