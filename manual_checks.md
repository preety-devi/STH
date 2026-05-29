# Manual Checks / Tests

## Test 1 — Add Item

Steps:

1. Open program
2. Select Add Item
3. Enter item name:
   Plastic Chair
4. Enter quantity:
   100

Expected Result:

* Item added successfully message appears
* Item is visible in inventory

---

## Test 2 — Duplicate Item Prevention

Steps:

1. Add item:
   Plastic Chair
2. Try adding:
   Plastic Chair again

Expected Result:

* Program shows:
  "Item already exists."

---

## Test 3 — Search Functionality

Steps:

1. Open View / Search Items
2. Search using:

   * plastic
   * PLASTIC
   * chair

Expected Result:

* Matching item appears correctly in all cases

---

## Test 4 — Update Quantity

Steps:

1. Search item
2. Select matching item
3. Choose Update Quantity
4. Enter new quantity

Expected Result:

* Quantity updates successfully
* Updated value appears in inventory

---

## Test 5 — Delete Item

Steps:

1. Search item
2. Select item
3. Choose Delete
4. Confirm deletion using:
   y

Expected Result:

* Item deleted successfully message appears
* Deleted item no longer exists in inventory

---

## Test 6 — Delete Cancellation

Steps:

1. Search item
2. Choose Delete
3. Enter:
   n

Expected Result:

* Delete cancelled message appears
* Item remains in inventory

---

## Test 7 — Data Persistence

Steps:

1. Add inventory item
2. Exit program
3. Reopen program
4. View inventory

Expected Result:

* Previously added data still exists

---

## Test 8 — Invalid Input Handling

Steps:

1. Enter empty item name
2. Enter negative quantity
3. Enter text instead of number

Expected Result:

* Program shows validation messages
* Program does not crash
