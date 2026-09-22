"""
Console Record-Management Application
--------------------------------------
Concepts:
- Data Types & Variables
- Conditional Statements & Loops
- Functions
- Exception Handling
- File I/O (JSON used for persistent storage)
- Menu-driven Console Application Design
"""

import json
import os

# ------------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------------
DATA_FILE = "records.json"   # File used to persist records between runs


# ------------------------------------------------------------------
# FILE I/O FUNCTIONS
# ------------------------------------------------------------------
def load_records():
    """
    Load records from the JSON file.
    Returns a list of dictionaries. If the file doesn't exist or is
    corrupted, returns an empty list (with proper exception handling).
    """
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            else:
                print("⚠ Warning: Data file format invalid. Starting fresh.")
                return []
    except json.JSONDecodeError:
        print("⚠ Warning: Data file is corrupted or empty. Starting fresh.")
        return []
    except (IOError, OSError) as e:
        print(f"⚠ Error reading file: {e}")
        return []


def save_records(records):
    """
    Save the current list of records to the JSON file.
    """
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(records, file, indent=4)
    except (IOError, OSError) as e:
        print(f"⚠ Error saving data: {e}")


# ------------------------------------------------------------------
# HELPER / VALIDATION FUNCTIONS
# ------------------------------------------------------------------
def get_valid_int(prompt):
    """
    Repeatedly prompt the user until a valid integer is entered.
    Demonstrates exception handling for invalid input.
    """
    while True:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Invalid input. Please enter a valid whole number.")


def get_non_empty_string(prompt):
    """
    Repeatedly prompt until the user enters a non-empty string.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def find_record_by_id(records, record_id):
    """
    Search the records list for a matching ID.
    Returns the record dictionary if found, else None.
    """
    for record in records:
        if record["id"] == record_id:
            return record
    return None


def generate_new_id(records):
    """
    Generate a new unique ID (1 more than the current maximum ID).
    """
    if not records:
        return 1
    return max(record["id"] for record in records) + 1


# ------------------------------------------------------------------
# CRUD FUNCTIONS
# ------------------------------------------------------------------
def add_record(records):
    """
    Add a new record to the records list.
    """
    print("\n--- Add New Record ---")
    new_id = generate_new_id(records)

    name = get_non_empty_string("Enter Name: ")
    age = get_valid_int("Enter Age: ")
    department = get_non_empty_string("Enter Department: ")
    contact = get_non_empty_string("Enter Contact Number: ")

    record = {
        "id": new_id,
        "name": name,
        "age": age,
        "department": department,
        "contact": contact
    }

    records.append(record)
    save_records(records)
    print(f"Record added successfully with ID: {new_id}")


def view_records(records):
    """
    Display all existing records in a tabular format.
    """
    print("\n--- All Records ---")
    if not records:
        print("No records found.")
        return

    print(f"{'ID':<5}{'Name':<20}{'Age':<6}{'Department':<20}{'Contact':<15}")
    print("-" * 66)
    for record in records:
        print(f"{record['id']:<5}{record['name']:<20}{record['age']:<6}"
              f"{record['department']:<20}{record['contact']:<15}")


def search_record(records):
    """
    Search for a record by ID or Name.
    """
    print("\n--- Search Record ---")
    print("1. Search by ID")
    print("2. Search by Name")
    choice = input("Enter choice: ").strip()

    if choice == "1":
        record_id = get_valid_int("Enter ID to search: ")
        record = find_record_by_id(records, record_id)
        if record:
            print("\n Record Found:")
            print(record)
        else:
            print("No record found with that ID.")

    elif choice == "2":
        name = get_non_empty_string("Enter Name to search: ").lower()
        found = [r for r in records if r["name"].lower() == name]
        if found:
            print(f"\n{len(found)} Record(s) Found:")
            for r in found:
                print(r)
        else:
            print("No record found with that name.")
    else:
        print("Invalid choice.")


def update_record(records):
    """
    Update an existing record based on ID.
    """
    print("\n--- Update Record ---")
    record_id = get_valid_int("Enter ID of record to update: ")
    record = find_record_by_id(records, record_id)

    if not record:
        print("No record found with that ID.")
        return

    print("Leave field blank to keep current value.")

    name = input(f"Name [{record['name']}]: ").strip()
    if name:
        record["name"] = name

    age = input(f"Age [{record['age']}]: ").strip()
    if age:
        try:
            record["age"] = int(age)
        except ValueError:
            print("Invalid age input. Keeping previous value.")

    department = input(f"Department [{record['department']}]: ").strip()
    if department:
        record["department"] = department

    contact = input(f"Contact [{record['contact']}]: ").strip()
    if contact:
        record["contact"] = contact

    save_records(records)
    print("Record updated successfully.")


def delete_record(records):
    """
    Delete a record based on ID.
    """
    print("\n--- Delete Record ---")
    record_id = get_valid_int("Enter ID of record to delete: ")
    record = find_record_by_id(records, record_id)

    if not record:
        print("No record found with that ID.")
        return

    confirm = input(f"Are you sure you want to delete record {record_id}? (y/n): ").strip().lower()
    if confirm == "y":
        records.remove(record)
        save_records(records)
        print("Record deleted successfully.")
    else:
        print("Deletion cancelled.")


# ------------------------------------------------------------------
# MENU-DRIVEN MAIN APPLICATION
# ------------------------------------------------------------------
def display_menu():
    print("\n===== RECORD MANAGEMENT SYSTEM =====")
    print("1. Add Record")
    print("2. View All Records")
    print("3. Search Record")
    print("4. Update Record")
    print("5. Delete Record")
    print("6. Exit")
    print("=====================================")


def main():
    records = load_records()

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        try:
            if choice == "1":
                add_record(records)
            elif choice == "2":
                view_records(records)
            elif choice == "3":
                search_record(records)
            elif choice == "4":
                update_record(records)
            elif choice == "5":
                delete_record(records)
            elif choice == "6":
                print("Exiting... Data has been saved")
                break
            else:
                print("Invalid choice. Please select between 1 and 6")
        except Exception as e:
            # Catch all safety net for any unexpected runtime error
            print(f"⚠ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()