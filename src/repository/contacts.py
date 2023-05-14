from datetime import date, datetime
from sqlalchemy.orm import Session

from src.database.models import Contact
from src.schemas import ContactModel, ContactName


async def validate_birthday(brth: date):
    bth_now = date(datetime.now().year, datetime.now().month, datetime.now().day)
    brth = date(
        bth_now.year if bth_now.month < brth.month else bth_now.year + 1 if bth_now.day < brth.day else bth_now.year,
        brth.month, brth.day)
    delta = bth_now - brth
    return delta.days


async def get_contacts(db: Session):
    return db.query(Contact).all()


async def get_contacts_by_birthdays(db: Session):
    contacts = db.query(Contact).all()
    contacts_list = []
    for contact in contacts:
        if 0 <= await validate_birthday(contact.birthday) <= 7:
            contacts_list.append(contact)
    return contacts_list


async def get_contact_by_id(contact_id: int, db: Session):
    return db.query(Contact).filter_by(id = contact_id).first()


async def get_contact_by_email(email, db: Session):
    return db.query(Contact).filter_by(email=email).first()


async def get_contact_by_name(contact_name, db: Session):
    return db.query(Contact).filter_by(name=contact_name).all()


async def get_contact_by_surname(contact_surname, db: Session):
    return db.query(Contact).filter_by(surname=contact_surname).all()


async def create_contact(body: ContactModel, db: Session):
    contact = Contact(**body.dict())
    db.add(contact)
    db.commit()
    return contact


async def update_contact(body: ContactModel, contact_id, db: Session):
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


async def remove_contact(contact_id, db: Session):
    contact = await get_contact_by_id(contact_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact