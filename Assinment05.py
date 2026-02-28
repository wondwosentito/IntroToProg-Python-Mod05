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
    file = open(FILE_NAME, "r")
    students = json.load(file)
except Exception as e:
    print("Error: There was a problem with reading the file,")
    print("Please check that the file exists and that it is in the json format, ")
    print("---Technical Error Message --")
    print(e.__doc__)
    print(e.__str__())
finally:
    if file is not None and file.closed == False:
        file.close()

# Present and Process the data
while (True):

    # Present the menu of choices
    print(MENU)
    menu_choice = input("What would you like to do? ")

    # Input user data
    if menu_choice == "1":  # This will not work if an integer
        try:
                student_first_name = input("Enter the student's first name: ")
                if not student_first_name.isalpha():
                    raise ValueError("First name should not contain numbers.")
                student_last_name = input("Enter the student's last name:")
                if not student_last_name.isalpha():
                    raise ValueError("Last name should not contain numbers: ")
                course_name = input("Enter the course name: ")
                student_data = {"FirstName": student_first_name,
                                "LastName": student_last_name,
                                "CourseName": course_name}
                students.append(student_data)
                print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")
        except ValueError as e:
            print("Error: There was a problem with reading the file,")
            print("Please check that the file exists and that it is in the json format, ")
            print("---Technical Error Message --")
            print(e.__doc__)
            print(e.__str__())
        except Exception as e:
            print("Error: There was a problem with your entered data,")
            print("---Technical Error Message --")
            print(e.__doc__)
            print(e.__str__())
        continue

    # Present the current data
    elif menu_choice == "2":

        # Process and display the data
        print("\n")
        print(f"Current data: {json.dumps(students, indent=2)}")
        print("_" * 50)
        continue

    # Save the data to a file

    elif menu_choice == "3":
        try:
            file = open(FILE_NAME, "w")
            json.dump(students, file, indent=2)
            file.close()

            print("The following data was saved to file:")
            for student in students:
                print(f"Student {student["FirstName"]},{student["LastName"]}"
                f"is enrolled in {student["CourseName"]}")

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


