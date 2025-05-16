from datetime import datetime

class Student:
    def __init__(self, name):
        self.name = name
        self._enrollments = []
        self._grades = {}

    def enroll(self, course):
        if isinstance(course, Course):
            enrollment = Enrollment(self, course)
            self._enrollments.append(enrollment)
            course.add_enrollment(enrollment)
        else:
            raise TypeError("course must be an instance of Course")

    def get_enrollments(self):
        return self._enrollments.copy()

    def set_grade(self, enrollment, grade):
        if isinstance(enrollment, Enrollment) and enrollment in self._enrollments:
            self._grades[enrollment] = grade
        else:
            raise ValueError("Invalid enrollment or not associated with this student")

    def course_count(self):
        return len(self._enrollments)

    def aggregate_average_grade(self):
        if not self._grades:
            return 0.0
        total_grades = sum(self._grades.values())
        num_courses = len(self._grades)
        average_grade = total_grades / num_courses
        return average_grade

class Course:
    def __init__(self, title):
        self.title = title
        self._enrollments = []

    def add_enrollment(self, enrollment):
        if isinstance(enrollment, Enrollment):
            self._enrollments.append(enrollment)
        else:
            raise TypeError("enrollment must be an instance of Enrollment")

    def get_enrollments(self):
        return self._enrollments.copy()

class Enrollment:
    all = []
    
    def __init__(self, student, course):
        if isinstance(student, Student) and isinstance(course, Course):
            self.student = student
            self.course = course
            self._enrollment_date = datetime.now()
            type(self).all.append(self)
        else:
            raise TypeError("Invalid types for student and/or course")

    def get_enrollment_date(self):
        return self._enrollment_date

    @classmethod
    def aggregate_enrollments_per_day(cls):
        enrollment_count = {}
        for enrollment in cls.all:
            date = enrollment.get_enrollment_date().date()
            enrollment_count[date] = enrollment_count.get(date, 0) + 1
        return enrollment_count
    
    # Test script
def test_aggregate_methods():
    # Create students and courses
    student1 = Student("Alice")
    student2 = Student("Bob")
    course1 = Course("Math")
    course2 = Course("Science")
    course3 = Course("History")

    # Enroll students
    student1.enroll(course1)  # Enrollment 1
    student1.enroll(course2)  # Enrollment 2
    student2.enroll(course2)  # Enrollment 3
    student2.enroll(course3)  # Enrollment 4

    # Assign grades to student1
    enrollments1 = student1.get_enrollments()
    student1.set_grade(enrollments1[0], 85)  # Math
    student1.set_grade(enrollments1[1], 90)  # Science

    # Assign grades to student2
    enrollments2 = student2.get_enrollments()
    student2.set_grade(enrollments2[0], 78)  # Science
    student2.set_grade(enrollments2[1], 92)  # History

    # Test course_count
    print(f"Alice's course count: {student1.course_count()}")  # Expected: 2
    print(f"Bob's course count: {student2.course_count()}")    # Expected: 2

    # Test aggregate_average_grade
    print(f"Alice's average grade: {student1.aggregate_average_grade()}")  # Expected: (85 + 90) / 2 = 87.5
    print(f"Bob's average grade: {student2.aggregate_average_grade()}")    # Expected: (78 + 92) / 2 = 85.0

    # Test aggregate_enrollments_per_day
    print("Enrollments per day:", Enrollment.aggregate_enrollments_per_day())  # Expected: dictionary with today's date and count 4

# Run the test
test_aggregate_methods()
