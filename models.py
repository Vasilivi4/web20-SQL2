from faker import Faker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

import random

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    group_id = Column(Integer, ForeignKey("groups.id"))

    group = relationship("Group", back_populates="students")
    marks = relationship("Mark", back_populates="student")


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    students = relationship("Student", back_populates="group")


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    name = Column(String)


class Mark(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True)
    value = Column(Integer)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))

    student = relationship("Student", back_populates="marks")
    subject = relationship("Subject")


engine = create_engine("sqlite:///school.db")

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

fake = Faker()

students = []
for _ in range(30):
    student = Student(
        name=fake.name(), email=fake.email(), group_id=random.randint(1, 3)
    )
    students.append(student)

session.add_all(students)

groups = [Group(name=f"Group {i}") for i in range(1, 4)]

session.add_all(groups)

subjects = [Subject(name=fake.word()) for _ in range(5, 9)]

session.add_all(subjects)

teachers = []
for _ in range(3, 6):
    teacher = Teacher(name=fake.name())
    teachers.append(teacher)

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
