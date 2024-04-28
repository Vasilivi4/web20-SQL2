import argparse
from models import Teacher, Group, Subject, Student, Mark, engine, Base
from sqlalchemy.orm import sessionmaker

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def select_teachers():
    """List all teachers."""
    teachers = session.query(Teacher.id, Teacher.name).all()
    return teachers


def list_records(model):
    records = session.query(model).all()
    for record in records:
        print(f"ID: {record.id}, Name: {record.name}")


def create_record(model, **kwargs):
    obj = model(**kwargs)
    session.add(obj)
    session.commit()
    print(f"Record created: {obj}")


def update_record(model, record_id, **kwargs):
    obj = session.query(model).get(record_id)
    if obj:
        for key, value in kwargs.items():
            setattr(obj, key, value)
        session.commit()
        print(f"Record updated: {obj}")
    else:
        print(f"No record found with id={record_id}")


def remove_record(model, record_id):
    obj = session.query(model).get(record_id)
    if obj:
        session.delete(obj)
        session.commit()
        print(f"Record removed: {obj}")
    else:
        print(f"No record found with id={record_id}")


def create_record(model, **kwargs):
    obj = model(**kwargs)
    session.add(obj)
    session.commit()
    print(f"Record created: ID: {obj.id}, Name: {obj.name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CRUD operations for database models")
    parser.add_argument(
        "-a",
        "--action",
        choices=["create", "list", "update", "remove"],
        help="Action to perform",
        required=True,
    )
    parser.add_argument(
        "-m",
        "--model",
        choices=["Teacher", "Group", "Subject", "Student", "Mark"],
        help="Model to perform action on",
        required=True,
    )
    parser.add_argument("--id", help="ID of the record for update or remove actions")
    parser.add_argument("-n", "--name", help="Name for creating or updating a record")

    args = parser.parse_args()

    if args.action == "create":
        if args.name:
            create_record(globals()[args.model], name=args.name)
        else:
            print("Name argument is required for creating a record.")
    elif args.action == "list":
        list_records(globals()[args.model])
    elif args.action == "update":
        if args.id and args.name:
            update_record(globals()[args.model], args.id, name=args.name)
        else:
            print("ID and name arguments are required for updating a record.")
    elif args.action == "remove":
        if args.id:
            remove_record(globals()[args.model], args.id)
        else:
            print("ID argument is required for removing a record.")
