from faker import Faker
from .models import Department, StudentID, Student,Subject
import random
from .models import*

fake = Faker()

def create_subject_marks(n):
    try:
        student_objs = Student.objects.all()
        for student in student_objs:
            subjects= Subject.objects.all()
            for subject in subjects:
                SubjectMarks.objects.create(
                    subject = subject,
                    student = student,
                    marks = random.randint(0,100)

                )
    except Exception as e:
        print(e)    

def seed_db(n=10) -> None:
    used_emails = set()
    try:
        for _ in range(n):
            departments_objs = Department.objects.all()
            if not departments_objs.exists():
                print("No departments found. Please create some departments first.")
                return
            
            random_index = random.randint(0, len(departments_objs) - 1)
            department = departments_objs[random_index]
            student_id = f'STU-0{random.randint(100, 999)}'
            student_name = fake.name()
            
            student_email = fake.email()
            while student_email in used_emails:
                student_email = fake.email()
            used_emails.add(student_email)

            student_age = random.randint(20, 30)
            student_address = fake.address()

            student_id_obj = StudentID.objects.create(student_id=student_id)
            Student.objects.create(
                department=department,
                student_id=student_id_obj,
                student_name=student_name,
                student_email=student_email,
                student_age=student_age,
                student_address=student_address
            )
    except Exception as e:
        print(e)
