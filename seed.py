from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Subject, Teacher, Mark
import random

engine = create_engine("sqlite:///school.db")

Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

students = []
for _ in range(random.randint(30, 50)):
    student = Student(
        name=fake.name(), email=fake.email(), group_id=random.randint(1, 3)
    )
    students.append(student)

session.add_all(students)
session.commit()

groups = [Group(name=f"Group {i}") for i in range(1, 4)]

session.add_all(groups)
session.commit()

subjects = [Subject(name=fake.word()) for _ in range(random.randint(5, 8))]

session.add_all(subjects)
session.commit()

teachers = [Teacher(name=fake.name()) for _ in range(random.randint(3, 5))]

session.add_all(teachers)
session.commit()

for student in students:
    for subject in subjects:
        mark = Mark(
            value=random.randint(1, 10), student_id=student.id, subject_id=subject.id
        )
        session.add(mark)

session.commit()

print("Database seeded successfully.")
