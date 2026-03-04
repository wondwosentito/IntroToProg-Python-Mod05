# ------------------------------------------------------------------------------------------ #
# Title: Assignment 06
# Desc: This assignment demonstrates using constants, variables, functions, classes,
#       file IO (JSON), and structured exception handling using the Separation of Concerns pattern
# Change Log: (Who, When, What)
#   Wondwosen Paulos, 03/04/2026, Created Assignment06
# ------------------------------------------------------------------------------------------ #

import json


# -------------------------------------------- #
# Constants
# -------------------------------------------- #
MENU: str = """---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course
    2. Show current data  
    3. Save data to a file
    4. Exit the program
-----------------------------------------"""

FILE_NAME: str = "Enrollments.json"


# -------------------------------------------- #
# Variables
# -------------------------------------------- #
menu_choice: str = ""
students: list = []  # Two-dimensional list of dictionary rows (list of dicts)


# -------------------------------------------- #
# Classes
# -------------------------------------------- #
class FileProcessor:
    """Performs file processing tasks (reading from and writing to JSON files)."""

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """
        Reads JSON data from a file and loads it into the student_data list.

        Args:
            file_name (str): Name of the file to read.
            student_data (list): List to be filled with dictionary rows.

        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the JSON file has invalid format.
            Exception: For any other unexpected error.
        """
        try:
            with open(file_name, "r") as file:
                data = json.load(file)
                # Expecting a list of dicts; replace contents of student_data
                if isinstance(data, list):
                    student_data.clear()
                    student_data.extend(data)
                else:
                    raise ValueError("JSON file content must be a list of registrations (list of dictionaries).")
        except Exception:
            # Re-raise to let caller handle with structured error output
            raise

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """
        Writes student_data list as JSON into a file.

        Args:
            file_name (str): Name of the file to write.
            student_data (list): List of dictionary rows to save.

        Raises:
            PermissionError: If the file cannot be written due to permissions.
            TypeError: If the data is not JSON serializable.
            Exception: For any other unexpected error.
        """
        try:
            with open(file_name, "w") as file:
                json.dump(student_data, file, indent=2)
        except Exception:
            # Re-raise to let caller handle with structured error output
            raise


class IO:
    """Handles all input and output operations (UI layer) for the program."""

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        Displays a formatted error message (and optional technical details).

        Args:
            message (str): Friendly error message for the user.
            error (Exception, optional): Actual exception object, if available.
        """
        print("\n" + "*" * 60)
        print("ERROR:", message)
        if error is not None:
            print("Built-In Python error info:")
            print(type(error).__name__)
            print(error)
        print("*" * 60 + "\n")

    @staticmethod
    def output_menu(menu: str):
        """
        Displays the program menu.

        Args:
            menu (str): The menu string to display.
        """
        print(menu)

    @staticmethod
    def input_menu_choice():
        """
        Prompts the user for a menu choice and returns it.

        Returns:
            str: The user's menu choice.
        """
        return input("Please select an option (1-4): ").strip()

    @staticmethod
    def output_student_courses(student_data: list):
        """
        Displays student registrations as comma-separated values.

        Args:
            student_data (list): List of dictionary rows to display.
        """
        if not student_data:
            print("\nNo registrations to display.\n")
            return

        print("\nCurrent registrations:")
        for row in student_data:
            first = row.get("FirstName", "")
            last = row.get("LastName", "")
            course = row.get("CourseName", "")
            print(f"{first},{last},{course}")
        print()

    @staticmethod
    def input_student_data(student_data: list):
        """
        Prompts the user for student first name, last name, and course name.
        Adds the data as a dictionary row into student_data.

        Args:
            student_data (list): List of dictionary rows to append to.
        """
        # Structured error handling for first name
        while True:
            try:
                first_name = input("Enter the student's first name: ").strip()
                if not first_name:
                    raise ValueError("First name cannot be blank.")
                break
            except Exception as e:
                IO.output_error_messages("Please enter a valid first name.", e)

        # Structured error handling for last name
        while True:
            try:
                last_name = input("Enter the student's last name: ").strip()
                if not last_name:
                    raise ValueError("Last name cannot be blank.")
                break
            except Exception as e:
                IO.output_error_messages("Please enter a valid last name.", e)

        # Course name (not explicitly required for structured error handling)
        course_name = input("Enter the course name: ").strip()
        if not course_name:
            course_name = "Python"  # reasonable default

        student_data.append({"FirstName": first_name, "LastName": last_name, "CourseName": course_name})
        print("\nRegistration added.\n")


# -------------------------------------------- #
# Main Program
# -------------------------------------------- #
if __name__ == "__main__":
    # Read existing data on start
    try:
        FileProcessor.read_data_from_file(FILE_NAME, students)
    except Exception as e:
        IO.output_error_messages(
            f"Could not read from '{FILE_NAME}'. "
            f"Tip: Create the file and add starting JSON data (a list of dictionaries).",
            e
        )
        # Continue with empty list so program still runs
        students = []

    while True:
        IO.output_menu(MENU)
        menu_choice = IO.input_menu_choice()

        if menu_choice == "1":
            IO.input_student_data(students)

        elif menu_choice == "2":
            IO.output_student_courses(students)

        elif menu_choice == "3":
            try:
                FileProcessor.write_data_to_file(FILE_NAME, students)
                print("\nSaved to file. Data written:")
                IO.output_student_courses(students)
            except Exception as e:
                IO.output_error_messages(f"Could not write to '{FILE_NAME}'.", e)

        elif menu_choice == "4":
            print("\nGoodbye!\n")
            break

        else:
            print("\nPlease choose an option from 1 to 4.\n")




