from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Subject, Teacher, Mark, engine

Session = sessionmaker(bind=engine)
session = Session()


def select_1():
    """Find 5 students with the highest average score across all subjects."""
    students_with_avg_score = (
        session.query(
            Student.fullname, func.round(func.avg(Mark.value), 2).label("average_score")
        )
        .join(Mark, Student.id == Mark.student_id)
        .group_by(Student.id)
        .order_by(desc("average_score"))
        .limit(5)
        .all()
    )
    return students_with_avg_score


def select_2(subject_name):
    """Find the student with the highest average score for a specific subject."""
    student_with_highest_avg_score = (
        session.query(
            Student.fullname, func.round(func.avg(Mark.value), 2).label("average_score")
        )
        .join(Mark, Student.id == Mark.student_id)
        .join(Subject, Mark.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Student.id)
        .order_by(desc("average_score"))
        .first()
    )
    return student_with_highest_avg_score


def select_3(subject_name):
    """Find the average score in groups for a specific subject."""
    avg_score_by_group = (
        session.query(
            Group.name, func.round(func.avg(Mark.value), 2).label("average_score")
        )
        .join(Student, Group.id == Student.group_id)
        .join(Mark, Student.id == Mark.student_id)
        .join(Subject, Mark.subject_id == Subject.id)
        .filter(Subject.name == subject_name)
        .group_by(Group.name)
        .all()
    )
    return avg_score_by_group


# Add the rest of the select functions from select_4 to select_10 here


def select_4():
    """Find the average score across all marks."""
    average_score = session.query(
        func.round(func.avg(Mark.value), 2).label("average_score")
    ).scalar()
    return average_score


def select_5(teacher_name):
    """Find the courses taught by a specific teacher."""
    courses_taught = (
        session.query(Subject.name)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Teacher.name == teacher_name)
        .all()
    )
    return courses_taught


def select_6(group_name):
    """Find the list of students in a specific group."""
    students_in_group = (
        session.query(Student.fullname)
        .join(Group, Student.group_id == Group.id)
        .filter(Group.name == group_name)
        .all()
    )
    return students_in_group


def select_7(group_name, subject_name):
    """Find the marks of students in a specific group for a particular subject."""
    marks_in_group_for_subject = (
        session.query(Student.fullname, Mark.value)
        .join(Group, Student.group_id == Group.id)
        .join(Mark, Student.id == Mark.student_id)
        .join(Subject, Mark.subject_id == Subject.id)
        .filter(Group.name == group_name)
        .filter(Subject.name == subject_name)
        .all()
    )
    return marks_in_group_for_subject


def select_8(teacher_name):
    """Find the average score given by a specific teacher for their subjects."""
    average_score_by_teacher = (
        session.query(func.round(func.avg(Mark.value), 2).label("average_score"))
        .join(Subject, Mark.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .filter(Teacher.name == teacher_name)
        .scalar()
    )
    return average_score_by_teacher


def select_9(student_name):
    """Find the list of courses attended by a specific student."""
    courses_attended_by_student = (
        session.query(Subject.name)
        .join(Mark, Subject.id == Mark.subject_id)
        .join(Student, Mark.student_id == Student.id)
        .filter(Student.fullname == student_name)
        .all()
    )
    return courses_attended_by_student


def select_10(student_name, teacher_name):
    """Find the list of courses taught by a specific teacher to a specific student."""
    courses_taught_to_student_by_teacher = (
        session.query(Subject.name)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .join(Mark, Subject.id == Mark.subject_id)
        .join(Student, Mark.student_id == Student.id)
        .filter(Teacher.name == teacher_name)
        .filter(Student.fullname == student_name)
        .all()
    )
    return courses_taught_to_student_by_teacher


def select_additional_1(student_name, teacher_name):
    """Find the average score given by a specific teacher to a specific student."""
    average_score_by_teacher_to_student = (
        session.query(func.round(func.avg(Mark.value), 2).label("average_score"))
        .join(Subject, Mark.subject_id == Subject.id)
        .join(Teacher, Subject.teacher_id == Teacher.id)
        .join(Student, Mark.student_id == Student.id)
        .filter(Teacher.name == teacher_name)
        .filter(Student.fullname == student_name)
        .scalar()
    )
    return average_score_by_teacher_to_student


def select_additional_2(group_name, subject_name):
    """Find the marks of students in a specific group for a particular subject on the last lesson."""
    last_lesson_marks = (
        session.query(Student.fullname, Mark.value)
        .join(Group, Student.group_id == Group.id)
        .join(Mark, Student.id == Mark.student_id)
        .join(Subject, Mark.subject_id == Subject.id)
        .filter(Group.name == group_name)
        .filter(Subject.name == subject_name)
        .order_by(Mark.lesson_date.desc())
        .limit(1)
        .all()
    )
    return last_lesson_marks
