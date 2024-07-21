#!/usr/bin/python3

class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
        self.courses = {}

    def add_course(self, course_code, grade):
        self.courses[course_code] = grade

    def calculate_gpa(self):
        if not self.courses:
            return 0.0
        total_points = sum(self.courses.values())
        return total_points / len(self.courses)


class Course:
    def __init__(self, course_code, course_name):
        self.course_code = course_code
        self.course_name = course_name


class GradeBook:
    def __init__(self):
        self.students = {}
        self.courses = {}

    def create_student(self, student_id, name):
        if student_id in self.students:
            print("Student ID already exists.")
        else:
            self.students[student_id] = Student(student_id, name)
            print("Student record created.")

    def view_students(self):
        if not self.students:
            print("No student records available.")
        for student in self.students.values():
            print(f"ID: {student.student_id}, Name: {student.name}")

    def edit_student(self, student_id, new_name):
        if student_id in self.students:
            self.students[student_id].name = new_name
            print("Student record updated.")
        else:
            print("Student ID not found.")

    def create_course(self, course_code, course_name):
        if course_code in self.courses:
            print("Course code already exists.")
        else:
            self.courses[course_code] = Course(course_code, course_name)
            print("Course record created.")

    def register_student_course(self, student_id, course_code):
        if student_id in self.students and course_code in self.courses:
            self.students[student_id].add_course(course_code, 0.0)
            print("Student registered for course.")
        else:
            print("Invalid student ID or course code.")

    def register_grade(self, student_id, course_code, grade):
        if student_id in self.students and course_code in self.courses:
            self.students[student_id].add_course(course_code, grade)
            print("Grade registered.")
        else:
            print("Invalid student ID or course code.")

    def sort_students_by_gpa(self):
        sorted_students = sorted(self.students.values(), key=lambda s: s.calculate_gpa(), reverse=True)
        for student in sorted_students:
            print(f"ID: {student.student_id}, Name: {student.name}, GPA: {student.calculate_gpa():.2f}")

    def search_student_by_gpa(self, gpa):
        found = False
        for student in self.students.values():
            if abs(student.calculate_gpa() - gpa) < 0.01:
                print(f"ID: {student.student_id}, Name: {student.name}, GPA: {student.calculate_gpa():.2f}")
                found = True
        if not found:
            print("No student found with the specified GPA.")

    def generate_transcript(self, student_id):
        if student_id in self.students:
            student = self.students[student_id]
            print(f"Transcript for {student.name} (ID: {student.student_id}):")
            for course_code, grade in student.courses.items():
                print(f"{course_code}: {grade}")
            print(f"GPA: {student.calculate_gpa():.2f}")
        else:
            print("Student ID not found.")

    def menu(self):
        while True:
            print()
            print("========================================================================")
            print(" Welcome to the Grade Book Application, your comprehensive program for")
            print(" managing student records, course registration, and GPA calculations.")
            print("========================================================================")
            print()
            print("Select one of the options below based on what you need to accomplish now")
            print()
            print("0. Read the Grade Book Application's Introduction")
            print("1. Create Student Record")
            print("2. View Student Records")
            print("3. Edit Student Records")
            print("4. Create Course Record")
            print("5. Register Student for a Course")
            print("6. Register Student Grades")
            print("7. Sort Students by their GPA Rankings")
            print("8. Search Student by GPA obtained")
            print("9. Generate Students' Transcripts")
            print("10. Exit the Grade Book Application")

            choice = int(input("Enter your choice [0-10]: "))
            if choice == 0:
                try:
                    with open("README.md", "r") as file:
                        content = file.read()
                        print(content)
                except FileNotFoundError:
                    print("README.md file not found.")
                except Exception as e:
                    print(f"An error occurred: {e}")
            elif choice == 1:
                student_id = input("Enter student ID: ")
                name = input("Enter student name: ")
                self.create_student(student_id, name)
            elif choice == 2:
                self.view_students()
            elif choice == 3:
                student_id = input("Enter student ID to edit: ")
                new_name = input("Enter new student name: ")
                self.edit_student(student_id, new_name)
            elif choice == 4:
                course_code = input("Enter course code: ")
                course_name = input("Enter course name: ")
                self.create_course(course_code, course_name)
            elif choice == 5:
                student_id = input("Enter student ID: ")
                course_code = input("Enter course code: ")
                self.register_student_course(student_id, course_code)
            elif choice == 6:
                student_id = input("Enter student ID: ")
                course_code = input("Enter course code: ")
                grade = float(input("Enter grade: "))
                self.register_grade(student_id, course_code, grade)
            elif choice == 7:
                self.sort_students_by_gpa()
            elif choice == 8:
                gpa = float(input("Enter GPA to search: "))
                self.search_student_by_gpa(gpa)
            elif choice == 9:
                student_id = input("Enter student ID: ")
                self.generate_transcript(student_id)
            elif choice == 10:
                print("Exiting the Grade Book Application.")
                break
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    gradebook = GradeBook()
    gradebook.menu()
