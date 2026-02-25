# ------------------------------------------------------------------------------------------ #
# Title: Assignment 05
# Desc: This assignment demonstrates using dictionaries, files (JSON), and exception handling
# Change Log: (Who, When, What)
#   WPaulos, 02/24/2026, Created Assignment05.py
# ------------------------------------------------------------------------------------------ #

import json

# Constants
MENU: str = """---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course
    2. Show current data  
    3. Save data to a file
    4. Exit the program
----------------------------------------- 
"""
FILE_NAME: str = "Enrollments.json"

# Variables
student_first_name: str = ""
student_last_name: str = ""
course_name: str = ""
file = None
menu_choice: str = ""
student_data: dict = {}
students: list = []


# -----------------------------
# Read starting data from file
# -----------------------------
try:
    file = open(FILE_NAME, "r", encoding="utf-8")
    students = json.load(file)

    # Safety check: ensure we loaded a list
    if not isinstance(students, list):
        print("Warning: File data is not a list. Starting with an empty list.")
        students = []

    file.close()

except FileNotFoundError:
    # If file doesn't exist yet, start with empty list
    students = []
    if file is not None and file.closed is False:
        file.close()

except json.JSONDecodeError:
    # If file is empty or invalid JSON, start with empty list
    print("Warning: File contains invalid or empty JSON. Starting with an empty list.")
    students = []
    if file is not None and file.closed is False:
        file.close()

except Exception as e:
    print(f"Unexpected error reading {FILE_NAME}: {e}")
    students = []
    if file is not None and file.closed is False:
        file.close()


# -----------------------------
# Main Menu Loop
# -----------------------------
while True:
    print(MENU)
    menu_choice = input("What would you like to do?: ").strip()

    # Option 1: Register a student
    if menu_choice == "1":

        # Structured error handling for first name
        while True:
            try:
                student_first_name = input("Enter student's first name: ").strip()
                if student_first_name == "":
                    raise ValueError("First name cannot be empty.")
                break
            except ValueError as e:
                print(e)

        # Structured error handling for last name
        while True:
            try:
                student_last_name = input("Enter student's last name: ").strip()
                if student_last_name == "":
                    raise ValueError("Last name cannot be empty.")
                break
            except ValueError as e:
                print(e)

        course_name = input("Enter course name: ").strip()

        # Add data to dictionary, then add dictionary to list
        student_data = {
            "first_name": student_first_name,
            "last_name": student_last_name,
            "course_name": course_name
        }
        students.append(student_data)

        print(f"\nRegistered: {student_first_name} {student_last_name} for {course_name}\n")

    # Option 2: Show current data (comma-separated)
    elif menu_choice == "2":
        if len(students) == 0:
            print("\nNo registrations entered yet.\n")
        else:
            print("\nCurrent Data (CSV-style):")
            for row in students:
                print(f"{row['first_name']},{row['last_name']},{row['course_name']}")
            print()

    # Option 3: Save data to file (json.dump) and display what was written
    elif menu_choice == "3":
        try:
            file = open(FILE_NAME, "w", encoding="utf-8")
            json.dump(students, file, indent=2)
            file.close()

            print("\nThe following data was saved to file:")
            for row in students:
                print(f"{row['first_name']},{row['last_name']},{row['course_name']}")
            print()

        except Exception as e:
            print(f"\nError saving data to {FILE_NAME}: {e}\n")
            if file is not None and file.closed is False:
                file.close()

    # Option 4: Exit
    elif menu_choice == "4":
        print("\nProgram Ended")
        break

    else:
        print("\nPlease only choose option 1, 2, 3, or 4.\n")