# Project in Phases

I am dividing this project into phases so that I can build and test software incrementally instead of trying to implement the entire tent house system at once.

Each phase will:

-solve one clear problem,
-remain small enough to reason about,
-work end-to-end from the command line,
-persist data after restart,
-and be independently demoable.

This approach helps me:

-verify the core logic step by step,
-avoid mixing too many features together,
-keep the codebase understandable,
-and catch design mistakes early before the system becomes complex.

I will complete and test each phase fully before moving to the next one.



# Phase 1 — Basic Inventory Storage CLI

Purpose
Phase 1 focuses only on storing and managing inventory for one type of tent house item.
The purpose of this phase is to build the smallest possible working CLI application that:

-accepts inventory input from the user,
-stores it permanently in a JSON file,
-reloads the same data when restarted,
-and allows quantity updates.

This phase intentionally avoids all booking logic, date handling, money calculations, and availability checking.

The goal is to prove that the project structure, CLI flow, and JSON persistence work correctly before adding business complexity.

Problem Being Solved
In this phase, I want the software to behave like a small digital inventory register so that Rakesh ji should be able to keep a digital record of how many items exist in inventory instead of remembering everything manually.



Scope of Phase 1
This phase supports only one inventory item type.
Example:
Plastic Chairs
The program will NOT yet handle:

multiple categories,
bookings,
customers,
event dates,
returns,
damaged items,
payments,
delivery tracking.


Features Included
1. Add Inventory Item

The user can create a new inventory item by entering:
-item name
-quantity

Example:

Enter item name: Plastic Chair
Enter quantity: 100

The program stores this data in memory and writes it to a JSON file.

2. View Inventory

The user can see all saved inventory items.

Example output:
ID: 1
Item: Plastic Chair
Quantity: 100

This proves data is loading correctly from storage.

3. Update Quantity

The user can increase or decrease quantity for an existing item.

Example:

Enter item ID: 1
Enter new quantity: 120

The updated quantity should immediately save to the JSON file.

4. Persistent Storage Using JSON

I will save inventory data into a JSON file and reload it when the application starts again.

Example:

[
  {
    "item_id": 1,
    "item_name": "Plastic Chair",
    "quantity": 120
  }
]

Command Line Flow
When the program starts, the user should see:

1. Add Item
2. View Items
3. Update Quantity
4. Exit

The CLI should continue running until the user chooses Exit.

Internal Structure
Suggested modules:

main.py       -> CLI menu and user interaction
inventory.py  -> inventory operations
storage.py    -> JSON read/write logic

Responsibilities should remain separated so future phases can extend the project cleanly.

End-to-End Demo Scenario
The complete Phase 1 demo should work like this:

Step 1 - Start the application.

Step 2 -Add an item:

        Plastic Chair
        Quantity: 100

Step 3- View inventory and confirm item appears.

Step 4- Update quantity from 100 → 120.

Step 5- Exit the application.

Step 6- Restart the application.

Step 7- View inventory again and confirm:

         Plastic Chair still exists
         quantity is still 120

This demonstrates:

CLI works,
updates work,
JSON persistence works,
data survives restart.


Error Handling
-Phase 1 should handle simple invalid cases:
-quantity cannot be negative
-updating a non-existing item ID should show an error
-empty item name should not be accepted
-corrupted/missing JSON file should not crash the program
Simple text error messages are enough for this phase.


Tests/Checks
Phase 1 should include basic tests or manual verification for:

-adding inventory items
-viewing saved items
-updating quantities
-saving JSON correctly
-loading JSON after restart
-handling invalid input


Phase 1 is complete when:

-the CLI works end-to-end,
-inventory data persists after restart,
-all included operations behave correctly,
-invalid input is handled safely,
-the project remains small and understandable,
-and the phase can be demonstrated independently without needing future   phases.



# Phase 2 — Inventory Availability and Booking Dates
Purpose

In Phase 2, I will implement the core business problem of the tent house system: availability checking across booking dates.

This phase introduces booking management and date-based inventory allocation while still keeping the system intentionally small. The goal is to prove that the software can correctly determine whether inventory is available for a requested booking period and prevent overbooking.

Problem Being Solved
Rakesh ji’s business depends on answering one critical question quickly and correctly:
“Do we still have enough chairs available for these event dates?”
The software should now help prevent double-booking and overbooking.


Scope of Phase 2
This phase adds:
-booking creation,
-booking storage,
-customer details
-occasion selection
-function dates
-booking dates
-date handling,
-overlap checking,
-and availability validation.

This phase still does NOT include:
-payments,
-delivery/return tracking,
-damaged items,
-reports,
-or multiple item categories.

Features Included
1. Create Booking
The user can enter:

customer name
occasion
booking start date
booking end date
function start date
function end date
quantity required

Example:

Customer Name: Rahul
Occasion: Marriage
Booking Start Date: 2026-06-08
Booking End Date: 2026-06-13
Function Start Date: 2026-06-10
Function End Date: 2026-06-12
Quantity Required: 40


2. Occasion Selection
The system will support common tent house event types:

Marriage
Birthday Party
Reception
Grand Party
Corporate Event
Other

This helps make booking records more meaningful.

3. Date Validation

The system must validate:

correct date format (YYYY-MM-DD)
booking start date is before booking end date
function start date is before function end date
function dates fall within booking dates

Invalid date combinations will be rejected

4. Availability Checking

Before saving a booking, I will calculate:
-total inventory,
-already reserved quantity on overlapping dates,
-and remaining available quantity.
The booking will only succeed if enough inventory is available.

Overlap Detection

Availability calculations will use:
Booking Start Date
Booking End Date
because inventory is unavailable during the entire rental period, not just during the function itself.

Example:
Total Inventory:
100 Plastic Chairs
Existing Booking:
60 Chairs
Booking Dates:
10 June – 12 June
New Request:
50 Chairs
Booking Dates:
11 June – 13 June

Result:
Booking must be rejected because:
60 + 50 = 110
Available Inventory = 100
Therefore inventory is overbooked.

End-to-End Demo for Phase 2

I should be able to:

1 Create inventory items
2 Search inventory while booking
3 Create valid bookings
4 Reject overbooked bookings
5 Reject invalid date combinations
6 Restart the application
7 Confirm bookings persist correctly

This proves:
availability calculation works
overlap detection works
overbooking prevention works
search functionality works
persistence works
Tests / Checks

I will test:

valid booking creation
overlapping bookings
overbooking rejection
invalid booking dates
invalid function dates
case-insensitive item search
partial-name item search
persistence after restart
quantity validation

Phase 2 is Complete When

bookings can be created successfully
availability is calculated correctly
overlapping bookings are detected correctly
overbooking is prevented
booking and function dates are validated
inventory search works using partial and case-insensitive matching
all booking data persists correctly
the entire phase works independently end-to-end

# Phase 3 — Expanding Toward Real Tent House Operations

Purpose
After implementing inventory availability checking in Phase 2, I will gradually expand the system toward more realistic tent house operations.
Instead of adding all remaining features together in one large step, I will divide this phase into smaller independently demoable sub-phases.
This will help me:
-keep the codebase manageable,
-test each workflow separately,
-and ensure the application remains stable after every addition.

Step 1 — Multiple Inventory Item Types
Purpose

Until Phase 2, the system only supports one inventory item type.

In this sub-phase, I will extend the system to support multiple inventory items within the same booking.

Example items:

chairs
tables
tents
lights
Features Added

I will add:
-support for multiple inventory item types,
-bookings containing multiple items,
-and availability checking for each item independently.

Problem Being Solved
The owner should now be able to manage realistic bookings involving different tent house items instead of only one inventory type.

End-to-End Demo
I should be able to:
-create multiple inventory item types,
-create bookings containing different items,
-verify availability separately for each item,
-restart the application,
=and confirm all inventory and booking data persists correctly.

Tests/Checks

I will test:

multi-item bookings,
item-wise availability checking,
overlapping bookings for different items,
and persistence after restart.
Definition of Done

Step 1 is complete when:
bookings can contain multiple item types,
availability works correctly for each item,
and all data persists correctly after restart.

Step 2 — Customer Details and Payment Tracking
Purpose
In this sub-phase, I will add customer and payment information to bookings.
The goal is to help track:
who made the booking,
how much payment is required,
how much advance was paid,
and how much payment is still pending.
Features Added

I will add:
            customer contact details,
            booking payment amount,
            advance payment tracking,
            pending balance calculation,
            and payment status.


Problem Being Solved
The owner should now be able to track customer bookings and payment progress instead of managing payments manually.

End-to-End Demo
I should be able to:

                    create a booking with customer details,
                    record advance payment,
                    calculate remaining balance,
                    update payment status,
                    restart the application,
                    and confirm payment data persists correctly.

Tests/Checks
I will test:

            payment calculations,
            advance payment updates,
            pending balance calculations,
            and persistence after restart.


Step 2 is complete when:
customer information is stored correctly,
payment tracking works properly,
and payment data persists safely after restart.


Step 3 — Delivery and Return Tracking
Purpose
In this sub-phase, I will track delivery and return operations for booked inventory.
The goal is to monitor whether booked items:
were delivered,
were returned,
and became available again after return.
Features Added

I will add:
           delivery status,
           return status,
           booking status updates,
           and inventory updates after return.


Problem Being Solved
The owner should now be able to track the movement of inventory items instead of only booking information.

End-to-End Demo
I should be able to:
                   create a booking,
                   mark items as delivered,
                   mark items as returned,
                   verify returned inventory becomes available again,
                   restart the application,
                   and confirm delivery/return data persists correctly.

Tests/Checks
I will test:
            delivery status updates,
            return workflows,
            inventory restoration after return,
            and persistence after restart.


Step 3 is complete when:
delivery and return tracking work correctly,
inventory updates properly after returns,
and all operational data persists correctly.

Step 4 — Damaged Item Tracking
Purpose
In this sub-phase, I will handle damaged inventory items returned after events.
The goal is to prevent damaged inventory from incorrectly appearing as available inventory.

Features Added
I will add:
           damaged quantity recording,
           damage notes/reasons,
           and usable inventory reduction.


Problem Being Solved
The owner should now be able to separate usable inventory from damaged inventory.

End-to-End Demo
I should be able to:
                    mark returned items as damaged,
                    reduce usable inventory quantity,
                    prevent damaged inventory from being booked,
                    restart the application,
                    and confirm damage records persist correctly.

Tests/Checks
I will test:
damaged inventory recording,
inventory reduction after damage,
booking prevention for damaged stock,
and persistence after restart.


Step 4 is complete when:
damaged inventory is tracked correctly,
damaged items cannot be booked,
and inventory consistency remains correct after damage handling.


# Phase 4 — Error Handling and Real Wedding Season Scenarios
Purpose
In Phase 4, I will focus on finding business edge cases and making the software reliable under real-world conditions.

Instead of adding major new features, this phase focuses on robustness and correctness.

Problem Being Solved
Real tent house operations involve messy situations:
late returns,
damaged inventory,
incorrect booking edits,
invalid user input,
and heavy booking overlaps during wedding season.
This phase ensures the software behaves safely during such situations.


Improvements Added
I will improve:
validation,
error handling,
inventory consistency,
booking editing,
and data recovery behavior.


Example Edge Cases
I will test situations such as:

-returning more items than delivered,
-reducing inventory below already-booked quantity,
-editing overlapping bookings,
-invalid dates,
-corrupted JSON files,
-and duplicate booking mistakes.

End-to-End Demo for Phase 4
I should be able to:
-intentionally create invalid situations,
-show that the program prevents incorrect behavior,
-and prove that inventory consistency remains safe.


Tests/Checks
This phase will heavily focus on:
-edge-case testing,
-invalid input handling,
-business-rule validation,
-and system stability.


Phase 4 is complete when:
-the software safely handles edge cases,
-inventory consistency remains correct,
-and the application behaves reliably under invalid or stressful conditions.

# Phase 5 — Cleanup, Refactoring, and User Experience
Purpose

In Phase 5, I will improve the structure, readability, and usability of the project.

The goal is to convert the working prototype into software that is easier to maintain, understand, and use.

Improvements Added
In this phase, I will focus on:

-cleaning up code structure,
-improving CLI readability,
-reducing duplicated logic,
-improving menu flow,
-organizing modules better,
-improving naming and comments,
-and making the application easier to demo and understand.


Problem Being Solved
Even if software works technically, it becomes difficult to maintain if:

-the code is messy,
-menus are confusing,
-or the structure is unclear.
This phase improves overall software quality.

End-to-End Demo for Phase 5

I should be able to:

1 run the entire system smoothly,
2 demonstrate all major workflows clearly,
3 and explain the project structure cleanly.
The CLI should feel understandable and organized for both developers and users.



The project is complete when:
-all phases work together correctly,
-inventory and booking logic remain accurate,
-data persists safely,
-the CLI is understandable,
-and the software can realistically support basic tent house operations   end-to-end.