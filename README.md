# Sharma Tent House Inventory CLI

## Overview

This is a command-line based  management system built for Sharma Tent House.

The program allows the owner to:

* Add inventory items
* View and search inventory
* Update item quantities
* Delete inventory items
* Prevent duplicate entries
* Persist data using JSON storage

The system is designed to keep the workflow simple and user-friendly for daily tent house operations.

---

## How to Run the Program

Open terminal in the project folder and run:

```bash
python main.py
```

---

## Main Features

### Add Item

Users can add new inventory items with quantity.

### Duplicate Prevention

If an item already exists, the program prevents duplicate entry.

### View / Search Inventory

Users can:

* view all inventory items
* search items by name
* perform actions directly from search results

### Update Quantity

Users can update item quantities from the search results.

### Delete Item

Users can safely delete items with confirmation.

### Case-Insensitive Search

Search works with:

* lowercase
* uppercase
* partial names

Example:

* plastic
* PLASTIC
* Plastic Chair

All will match correctly.

### Data Persistence

Inventory data remains saved even after closing and reopening the program.

---

## Input Validation

The program handles:

* empty item names
* duplicate item names
* negative quantities
* invalid numeric input
* invalid menu choices
