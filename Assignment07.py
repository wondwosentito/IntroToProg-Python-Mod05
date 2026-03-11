# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
#   WPaulos 03/11/2026, Assignment07-Classes and Objects
# ------------------------------------------------------------------------------------------ #

import json
import _io

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str = ""  # Hold the choice made by the user.


# Data --------------------------------------- #
class Person:
    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if not value.isalpha():
            raise ValueError("First name should not contain numbers.")
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if not value.isalpha():
            raise ValueError("Last name should not contain numbers.")
        self.__last_name = value

    def __str__(self):
        return f"{self.first_name},{self.last_name}"


class Student(Person):
    def __init__(self, first_name: str, last_name: str, course_name: str):
        super().__init__(first_name, last_name)
        self.course_name = course_name

    @property
    def course_name(self):
        return self.__course_name

    @course_name.setter
    def course_name(self, value):
        self.__course_name = value

    def __str__(self):
        return f"{self.first_name},{self.last_name},{self.course_name}"


# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files
    """

    @staticmethod
    def read_data_from_file(file_name: str):
        """Reads data from a JSON file and returns a list of Student objects."""
        file = None
        student_objects = []

        try:
            file = open(file_name, "r")
            json_students = json.load(file)

            # Convert dictionary rows into Student objects
            for row in json_students:
                student = Student(
                    first_name=row["FirstName"],
                    last_name=row["LastName"],
                    course_name=row["CourseName"]
                )
                student_objects.append(student)

        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with reading the file.", error=e)

        finally:
            if file is not None and file.closed == False:
                file.close()

        return student_objects

    @staticmethod
    def write_data_to_file(file_name: str, student_data: list):
        """Writes Student objects to a JSON file."""
        file = None

        try:
            # Convert Student objects into dictionaries
            json_students = []
            for student in student_data:
                row = {
                    "FirstName": student.first_name,
                    "LastName": student.last_name,
                    "CourseName": student.course_name
                }
                json_students.append(row)

            file = open(file_name, "w")
            json.dump(json_students, file, indent=2)

            IO.output_student_and_course_names(student_data=student_data)

        except Exception as e:
            message = "Error: There was a problem with writing to the file.\n"
            message += "Please check that the file is not open by another program."
            IO.output_error_messages(message=message, error=e)

        finally:
            if file is not None and file.closed == False:
                file.close()


# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        print()
        print(menu)
        print()

    @staticmethod
    def input_menu_choice():
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1", "2", "3", "4"):
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())

        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        print("-" * 50)
        for student in student_data:
            print(f"Student {student.first_name} "
                  f"{student.last_name} is enrolled in {student.course_name}")
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        try:
            student_first_name = input("Enter the student's first name: ")
            if not student_first_name.isalpha():
                raise ValueError("The first name should not contain numbers.")

            student_last_name = input("Enter the student's last name: ")
            if not student_last_name.isalpha():
                raise ValueError("The last name should not contain numbers.")

            course_name = input("Please enter the name of the course: ")

            # Create a Student object instead of a dictionary
            student = Student(
                first_name=student_first_name,
                last_name=student_last_name,
                course_name=course_name
            )

            student_data.append(student)
            print()
            print(f"You have registered {student_first_name} {student_last_name} for {course_name}.")

        except ValueError as e:
            IO.output_error_messages(message="One of the values was not the correct type of data!", error=e)

        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)

        return student_data


# Start of main body

# Read the file data into a list of Student objects
students = FileProcessor.read_data_from_file(file_name=FILE_NAME)

# Present and Process the data
while True:
    IO.output_menu(menu=MENU)
    menu_choice = IO.input_menu_choice()

    if menu_choice == "1":
        students = IO.input_student_data(student_data=students)
        continue

    elif menu_choice == "2":
        IO.output_student_and_course_names(students)
        continue

    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    elif menu_choice == "4":
        break

    else:
        print("Please only choose option 1, 2, or 3")

print("Program Ended")
