from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Subject, Teacher, Mark
import random

# Создаем соединение с базой данных
engine = create_engine("sqlite:///school.db")

# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Инициализируем Faker для создания случайных данных
fake = Faker()

# Создаем студентов
students = []
for _ in range(random.randint(30, 50)):
    student = Student(
        name=fake.name(), email=fake.email(), group_id=random.randint(1, 3)
    )
    students.append(student)

# Добавляем студентов в сессию
session.add_all(students)
session.commit()

# Создаем группы
groups = [Group(name=f"Group {i}") for i in range(1, 4)]

# Добавляем группы в сессию
session.add_all(groups)
session.commit()

# Создаем предметы
subjects = [Subject(name=fake.word()) for _ in range(random.randint(5, 8))]

# Добавляем предметы в сессию
session.add_all(subjects)
session.commit()

# Создаем преподавателей
teachers = [Teacher(name=fake.name()) for _ in range(random.randint(3, 5))]

# Добавляем преподавателей в сессию
session.add_all(teachers)
session.commit()

# Заполняем оценки для каждого студента по каждому предмету
for student in students:
    for subject in subjects:
        mark = Mark(
            value=random.randint(1, 10), student_id=student.id, subject_id=subject.id
        )
        session.add(mark)

# Коммитим изменения в базу данных
session.commit()

print("Database seeded successfully.")
