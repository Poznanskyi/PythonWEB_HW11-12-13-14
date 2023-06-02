from datetime import date, datetime
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel


async def validate_birthday(brth: date):
    """
    The validate_birthday function takes a date object as an argument and returns the number of days until that birthday.
        If the birthday has already passed this year, it will return the number of days until next year's birthday.

    :param brth: date: Pass the user's birthday into the function
    :return: The number of days until the user's birthday
    :doc-author: Poznanskyi
    """
    bth_now = date(datetime.now().year, datetime.now().month, datetime.now().day)
    brth = date(
        bth_now.year if bth_now.month < brth.month else bth_now.year + 1 if bth_now.day < brth.day else bth_now.year,
        brth.month, brth.day)
    delta = bth_now - brth
    return delta.days


async def get_contacts(db: Session):
    """
    The get_contacts function returns a list of all contacts in the database.

    :param db: Session: Pass the database session to the function
    :return: A list of contact objects
    :doc-author: Poznanskyi
    """
    return db.query(Contact).all()


async def get_contacts_by_birthdays(db: Session):
    """
        The get_contacts_by_birthdays function returns a list of contacts whose birthdays are within the next 7 days.

        :param db: Session: Pass the database session to the function
        :return: A list of contacts whose birthday is within the next 7 days
        :doc-author: Poznanskyi
        """
    contacts = db.query(Contact).all()
    contacts_list = []
    for contact in contacts:
        if 0 <= await validate_birthday(contact.birthday) <= 7:
            contacts_list.append(contact)
    return contacts_list


async def get_contact_by_id(contact_id: int, db: Session):
    """
    The get_contact_by_id function returns a contact from the database by its id.

    :param contact_id: int: Specify the id of the contact to be returned
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Poznanskyi
    """
    return db.query(Contact).filter_by(id = contact_id).first()


async def get_contact_by_email(email, db: Session):
    """
    The get_contact_by_email function returns a contact object from the database based on the email address provided.
        Args:
            email (str): The email address of the contact to be retrieved.
            db (Session, optional): SQLAlchemy Session instance. Defaults to None.

    :param email: Filter the query
    :param db: Session: Pass the database session to the function
    :return: The first contact found by the email address
    :doc-author: Poznanskyi
    """
    return db.query(Contact).filter_by(email=email).first()


async def get_contact_by_name(contact_name, db: Session):
    """
    The get_contact_by_name function returns a list of contacts that match the contact_name parameter.


    :param contact_name: Filter the database query
    :param db: Session: Pass the database session to the function
    :return: All contacts with the name specified in the contact_name parameter
    :doc-author: Poznanskyi
    """
    return db.query(Contact).filter_by(name=contact_name).all()


async def get_contact_by_surname(contact_surname, db: Session):
    """
    The get_contact_by_surname function returns a list of contacts with the given surname.

    :param contact_surname: Filter the query
    :param db: Session: Pass in the database session to the function
    :return: A list of contacts with the given surname
    :doc-author: Poznanskyi
    """
    return db.query(Contact).filter_by(surname=contact_surname).all()


async def create_contact(body: ContactModel, db: Session):
    """
    The create_contact function creates a new contact in the database.

    :param body: ContactModel: Pass the data from the request body to the function
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Poznanskyi
    """
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    return contact


async def update_contact(body: ContactModel, contact_id, db: Session):
    """
    The update_contact function updates a contact in the database.
        Args:
            body (ContactModel): The updated contact information.
            db (Session): A connection to the database.

    :param body: ContactModel: Get the data from the request body
    :param contact_id: Get the contact from the database
    :param db: Session: Pass the database session to the function
    :return: A contact
    :doc-author: Poznanskyi
    """
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        contact.name = body.name
        contact.surname = body.surname
        contact.email = body.email
        contact.birthday = body.birthday
        contact.phone = body.phone
        contact.description = body.description
        db.commit()
    return contact


async def remove_contact(contact_id: int, db: Session):
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            db (Session): A connection to the database.

    :param contact_id: Find the contact in the database
    :param db: Session: Pass in the database session to the function
    :return: The contact that was deleted
    :doc-author: Poznanskyi
    """
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact