#!/usr/bin/python3

import json
import os
import re

class Student:
    def __init__(self, email, name):
        self.email = email
        self.name = name
        self.courses = []
        self.gpa = 0.0

    def calculate_gpa(self):
        total_points = 0
        total_credits = 0

        # Calculate GPA based on grades and credits
        for course, grade, credits_earned in self.courses:
            total_points += grade * credits_earned
            total_credits += credits_earned
        self.gpa = total_points / total_credits if total_credits > 0 else 0.0

    def register_for_course(self, course, grade, credits_earned):
        self.courses.append((course, grade, credits_earned))
        self.calculate_gpa()

class Course:
    def __init__(self, name, trimester):
        self.name = name
        self.trimester = trimester

class GradeBook:
    def __init__(self):
        self.student_list = []
        self.course_list = []

    def add_student(self, email, name):
        if self.is_valid_email(email):
            if not any(s.email == email for s in self.student_list):
                new_student = Student(email, name)
                self.student_list.append(new_student)
                self.save_data()
                print("Student record created successfully.")
            else:
                print("A student with this email already exists.")
        else:
            print("Invalid email format.")

    def add_course(self, name, trimester):
        new_course = Course(name, trimester)
        self.course_list.append(new_course)
        self.save_data()

    def enter_student_grades_for_course(self, email, course_name, grade, credits_earned):
        student = next((s for s in self.student_list if s.email == email), None)
        course = next((c for c in self.course_list if c.name == course_name), None)
        if student and course:
            student.register_for_course(course_name, grade, credits_earned)
            self.save_data()
            print("Student grades entered successfully.")
        else:
            print("Student or course not found.")

    def calculate_ranking(self):
        # Sort students by GPA in descending order
        self.student_list.sort(key=lambda s: s.gpa, reverse=True)
        self.save_data()
        self.display_students_sorted_by_gpa()

    def display_students_sorted_by_gpa(self):
        print("Students sorted by GPA:")
        for student in self.student_list:
            print(f"Email: {student.email}, Name: {student.name}, GPA: {student.gpa:.2f}")

    def search_by_gpa(self, min_gpa, max_gpa):
        # Ensure GPA range is between 1 and 5
        if 1 <= min_gpa <= 5 and 1 <= max_gpa <= 5:
            return [s for s in self.student_list if min_gpa <= s.gpa <= max_gpa]
        else:
            print("Invalid GPA range. Please enter values between 1 and 5.")
            return []

    def generate_all_transcripts(self):
        transcripts = []
        for student in self.student_list:
            transcript = f"Transcript for {student.name} ({student.email}):\n"
            for course, grade, credits_earned in student.courses:
                transcript += f"Course: {course}, Grade: {grade}, Credits Earned: {credits_earned}\n"
            transcript += f"GPA: {student.gpa:.2f}\n"
            transcripts.append(transcript)
        return transcripts

    def is_valid_email(self, email):
        # Validate email format using regex
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    def save_data(self):
        # Save student and course data to JSON files
        with open('students.json', 'w') as f:
            json.dump([{'email': s.email, 'name': s.name, 'courses': s.courses, 'gpa': s.gpa} for s in self.student_list], f)
        with open('courses.json', 'w') as f:
            json.dump([c.__dict__ for c in self.course_list], f)

    def load_data(self):
        # Load student and course data from JSON files
        if os.path.exists('students.json'):
            with open('students.json', 'r') as f:
                students_data = json.load(f)
                self.student_list = [self._create_student_with_courses(data) for data in students_data]
                # Recalculate GPA for each student after loading
                for student in self.student_list:
                    student.calculate_gpa()
        if os.path.exists('courses.json'):
            with open('courses.json', 'r') as f:
                courses_data = json.load(f)
                self.course_list = [Course(**data) for data in courses_data]

    def _create_student_with_courses(self, data):
        student = Student(data['email'], data['name'])
        student.courses = data['courses']
        student.gpa = data['gpa']
        return student

def display_menu():
    print()
    print("========================================================================")
    print(" Welcome to the Grade Book Application, your comprehensive program for")
    print(" managing student records, course registration, and GPA calculations.")
    print("========================================================================")
    print()
    print("Select one of the options below based on what you need to accomplish now")
    print("0. Read the Grade Book Application's Introduction")
    print("1. Create Student Record")
    print("2. View Student Records")
    print("3. Edit Student Records")
    print("4. Create Course Record")
    print("5. Enter Student Grades for a Course")
    print("6. Display Students by their GPA Rankings")
    print("7. Search Student by GPA obtained")
    print("8. Generate Students' Transcripts")
    print("9. Exit the Grade Book Application")
    print()
    print("Enter your choice [0-9]:", end=" ")

def main():
    gradebook = GradeBook()
    gradebook.load_data()

    while True:
        display_menu()
        try:
            choice = int(input().strip())
        except ValueError:
            print("Invalid input. Please enter a number between 0 and 9.")
            continue

        if choice == 0:
            if os.path.exists('README.md'):
                with open('README.md', 'r') as file:
                    print(file.read())
            else:
                print("README.md file not found.")
        elif choice == 1:
            email = input("Enter student email: ").strip()
            name = input("Enter student name: ").strip()
            gradebook.add_student(email, name)
        elif choice == 2:
            for student in gradebook.student_list:
                print(f"Email: {student.email}, Name: {student.name}, GPA: {student.gpa:.2f}")
        elif choice == 3:
            email = input("Enter student email to edit: ").strip()
            student = next((s for s in gradebook.student_list if s.email == email), None)
            if student:
                name = input(f"Enter new name for {student.name} (leave blank to keep current): ").strip()
                if name:
                    student.name = name
                gradebook.save_data()
                print("Student record updated successfully.")
            else:
                print("Student not found.")
        elif choice == 4:
            name = input("N.B: In this coming trimester, we will teach students three mandatory courses [Frontend Web Development, Web Infrastructure, and Responsible Enterprise]. Therefore you are requested to register yourself in all of them.  Enter course name: ").strip()
            trimester = input("N.B: The coming trimester will begin in September this current year. Therefore, use 'September 2024' as the course trimester name. Enter course trimester: ").strip()
            gradebook.add_course(name, trimester)
            print("Course record created successfully.")
        elif choice == 5:
            email = input("Enter student email: ").strip()
            if not any(s.email == email for s in gradebook.student_list):
                print("Email not found. Please enter a valid student email.")
                continue
            course_name = input("Enter course name: ").strip()
            try:
                grade = int(input("Enter grade [1-5]: ").strip())
                credits_earned = int(input("Enter credits earned [0 or 25]: ").strip())
                # Validate grade and credits earned input
                if grade < 1 or grade > 5:
                    print("Invalid grade. Please enter a number between 1 and 5.")
                elif credits_earned not in [0, 25]:
                    print("Invalid credits. Please enter either 0 or 25.")
                else:
                    gradebook.enter_student_grades_for_course(email, course_name, grade, credits_earned)
            except ValueError:
                print("Invalid input. Please enter valid numbers for grade and credits earned.")
        elif choice == 6:
            gradebook.calculate_ranking()
        elif choice == 7:
            try:
                min_gpa = float(input("Enter minimum GPA (1-5): ").strip())
                max_gpa = float(input("Enter maximum GPA (1-5): ").strip())
                # Validate GPA range input
                if min_gpa < 1 or min_gpa > 5 or max_gpa < 1 or max_gpa > 5:
                    print("Invalid GPA range. Please enter values between 1 and 5.")
                else:
                    filtered_students = gradebook.search_by_gpa(min_gpa, max_gpa)
                    for student in filtered_students:
                        print(f"Email: {student.email}, Name: {student.name}, GPA: {student.gpa:.2f}")
            except ValueError:
                print("Invalid input. Please enter valid numbers for GPA range.")
        elif choice == 8:
            transcripts = gradebook.generate_all_transcripts()
            for transcript in transcripts:
                print(transcript)
        elif choice == 9:
            print("Exiting the Grade Book Application. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 0 and 9.")

if __name__ == "__main__":
    main()
