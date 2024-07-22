#!/usr/bin/python3

class Student:
    def __init__(self, email, names):
        self.email = email
        self.names = names
        self.courses_registered = {}
        self.gpa = 0.0

    def add_course(self, course_code, credits_earned, grade):
        self.courses_registered[course_code] = {'credits_earned': credits_earned, 'grade': grade}

    def calculate_gpa(self):
        total_credits = sum(course['credits_earned'] for course in self.courses_registered.values())
        if total_credits == 0:
            return 0.0
        total_points = sum(course['grade'] * course['credits_earned'] for course in self.courses_registered.values())
        self.gpa = total_points / total_credits
        return self.gpa

class Course:
    def __init__(self, name, trimester, credits_to_be_attempted):
        self.name = name
        self.trimester = trimester
        self.credits_to_be_attempted = credits_to_be_attempted

class GradeBook:
    def __init__(self):
        self.student_list = []
        self.course_list = []

    def add_student(self):
        email = input("Enter student email: ")
        names = input("Enter student names: ")
        new_student = Student(email, names)
        self.student_list.append(new_student)
        print("Student record created.")

    def add_course(self):
        name = input("N.B: In this upcoming trimester, we will teach these three courses [Fronted Web Development, Web Infrastructure, and Responsible Enterprise.] These courses are all mandatory, therefore register all of them and use '25' for each one as its 'credits to be attempted.' Enter course name: ")
        trimester = input("N.B: This upcoming trimester will begin in September 2024. Therefore, use 'september 2024' as the trimester name. Enter trimester: ")
        credits_to_be_attempted = float(input("Enter course credits to be attempted: "))
        new_course = Course(name, trimester, credits_to_be_attempted)
        self.course_list.append(new_course)
        print("Course record created.")

    def Enter_Student_Grades_for_a_Course(self):
        student_email = input("Enter student email: ")
        course_name = input("Enter course name: ")
        grade = float(input("N.B: Grades range in a [1-5] scale. Enter grade: "))
        credits_earned = float(input("N.B: If the student got a passmark, credits earned is the same as credits to be attempted. Otherwise, the value is 0. Enter credits earned: "))
        course = next((c for c in self.course_list if c.name == course_name), None)
        student = next((s for s in self.student_list if s.email == student_email), None)

        if student and course:
            student.add_course(course.name, credits_earned, grade)
            print("Student registered for course and grades have been well kept.")
        else:
            print("Invalid student email or course name.")

    def calculate_gpa(self):
        for student in self.student_list:
            student.calculate_gpa()

    def calculate_ranking(self):
        self.calculate_gpa()
        sorted_students = sorted(self.student_list, key=lambda s: s.gpa, reverse=True)
        for student in sorted_students:
            print(f"Email: {student.email}, GPA: {student.gpa:.2f}")

    def search_by_grade(self):
        lower_bound = float(input("Enter lower GPA bound [1-5]: "))
        upper_bound = float(input("Enter upper GPA bound [1-5]: "))
        filtered_students = [s for s in self.student_list if lower_bound <= s.gpa <= upper_bound]
        for student in filtered_students:
            print(f"Email: {student.email}, GPA: {student.gpa:.2f}")

    def generate_transcript(self):
        student_email = input("Enter student email: ")
        student = next((s for s in self.student_list if s.email == student_email), None)

        if student:
            print(f"Transcript for {student.names} (Email: {student.email}):")
            for course_code, details in student.courses_registered.items():
                print(f"{course_code}: {details['grade']} (Credits Earned: {details['credits_earned']})")
            print(f"GPA: {student.gpa:.2f}")
        else:
            print("Student email not found.")

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
            print("5. Enter Student Grades for a Course")
            print("6. Sort Students by their GPA Rankings")
            print("7. Search Student by GPA obtained")
            print("8. Generate Students' Transcripts")
            print("9. Exit the Grade Book Application")
            print()

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
                self.add_student()
            elif choice == 2:
                for student in self.student_list:
                    print(f"Email: {student.email}, Names: {student.names}")
            elif choice == 3:
                email = input("Enter student email to edit: ")
                new_names = input("Enter new student names: ")
                student = next((s for s in self.student_list if s.email == email), None)
                if student:
                    student.names = new_names
                    print("Student record updated.")
                else:
                    print("Student email not found.")
            elif choice == 4:
                self.add_course()
            elif choice == 5:
                self.Enter_Student_Grades_for_a_Course()
            elif choice == 6:
                self.calculate_ranking()
            elif choice == 7:
                self.search_by_grade()
            elif choice == 8:
                self.generate_transcript()
            elif choice == 9:
                print("Exiting the Grade Book Application.")
                break
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    gradebook = GradeBook()
    gradebook.menu()
