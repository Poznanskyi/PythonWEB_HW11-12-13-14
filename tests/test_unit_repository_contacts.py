import unittest
from unittest.mock import MagicMock
from datetime import date, datetime

from pydantic import EmailStr
from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel
from src.repository.contacts import (
    get_contacts,
    get_contacts_by_birthdays,
    get_contact_by_id,
    get_contact_by_email,
    get_contact_by_name,
    get_contact_by_surname,
    create_contact,
    update_contact,
    remove_contact
)


class TestNotes(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().all.return_value = contacts
        result = await get_contacts(db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_id(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = contact
        result = await get_contact_by_id(contact_id=1, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contacts_by_birthdays(self):
        contact = [Contact(birthday=date(datetime.now().year, datetime.now().month, datetime.now().day))]
        self.session.query().all.return_value = contact
        result = await get_contacts_by_birthdays(db=self.session)
        print(f'RESULT ______ {result}')
        self.assertEqual(result, contact)

    async def test_get_contact_by_email(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = contact
        result = await get_contact_by_email(email=f'aaa@gmail.com', db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_by_name(self):
        contact = [Contact()]
        self.session.query().filter_by().all.return_value = contact
        result = await get_contact_by_name(contact_name='Grigory', db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_by_surname(self):
        contact = [Contact()]
        self.session.query().filter_by().all.return_value = contact
        result = await get_contact_by_surname(contact_surname='Skovoroda', db=self.session)
        self.assertEqual(result, contact)

    async def test_create_contact(self):
        body = ContactModel(name="Grigory",
                            surname="Skovoroda",
                            email=EmailStr('aaa@gmail.com'),
                            phone='012345678',
                            birthday=date(datetime.now().year, datetime.now().month, datetime.now().day),
                            description='Nothing')
        result = await create_contact(body=body, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.description, body.description)

    async def test_remove_contact(self):
        contact = Contact(id=1)
        self.session.query().filter_by().first.return_value = contact
        result = await remove_contact(contact_id=1, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact(self):
        body = ContactModel(name="Grigory",
                            surname="Skovoroda",
                            email=EmailStr('aaa@gmail.com'),
                            phone='0112345678',
                            birthday=date(datetime.now().year, datetime.now().month, datetime.now().day),
                            description='Nothing',
                            id=1)
        contact = Contact(id=1)
        self.session.query().filter_by().first.return_value = contact
        print(self.session.query().filter_by().first.return_value.name)
        result = await update_contact(body=body, contact_id=1, db=self.session)
        self.assertEqual(result.name, body.name)
        self.assertEqual(result.surname, body.surname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.description, body.description)
        print(self.session.query().filter_by().first.return_value.name)


if __name__ == '__main__':
    unittest.main()