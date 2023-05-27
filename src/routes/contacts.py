from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import List

from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactResponse, ContactModel
from src.repository import contacts as repository_contacts
from src.database.models import Role, User
from src.services.auth import auth_service
from src.services.roles import RolesAccess

router = APIRouter(prefix='/contacts', tags=['contacts'])

access_get = RolesAccess([Role.admin, Role.moderator, Role.user])
access_create = RolesAccess([Role.admin, Role.moderator])
access_update = RolesAccess([Role.admin, Role.moderator])
access_delete = RolesAccess([Role.admin])


@router.get('/', response_model=List[ContactResponse], dependencies=[Depends(access_get)])
async def get_contacts(db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts(db)
    return contacts


@router.get('/birthdays', response_model=List[ContactResponse], dependencies=[Depends(access_get)])
async def get_contacts_by_birthdays(db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    contacts = await repository_contacts.get_contacts_by_birthdays(db)
    return contacts


@router.get('/{contact_id}', response_model=ContactResponse, dependencies=[Depends(access_get)])
async def get_contact_by_id(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                            _: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_id(contact_id, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such contact")
    return contact


@router.get('/search_by_name/{contact_name}', response_model=List[ContactResponse], dependencies=[Depends(access_get)])
async def get_contact_by_name(contact_name: str, db: Session = Depends(get_db),
                              _: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_name(contact_name, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such contact")
    return contact


@router.get('/search_by_surname/{contact_surname}', response_model=List[ContactResponse],
            dependencies=[Depends(access_get)])
async def get_contact_by_surname(contact_surname: str, db: Session = Depends(get_db),
                                 _: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_surname(contact_surname, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such contact")
    return contact


@router.get('/search_by_email/{contact_email}', response_model=ContactResponse, dependencies=[Depends(access_get)])
async def get_contact_by_email(contact_email: str, db: Session = Depends(get_db),
                               _: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_email(contact_email, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already exists')
    return contact


@router.post('/', response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(access_get)])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),
                         _: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.get_contact_by_email(body.email, db)
    if contact:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Email already exists')
    contact = await repository_contacts.create_contact(body, db)
    return contact


@router.put('/{contact_id}', response_model=ContactResponse, dependencies=[Depends(access_get)])
async def update_contact(body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         _: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.update_contact(body, contact_id, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such contact")
    return contact


@router.delete('/{contact_id}', response_model=ContactResponse, dependencies=[Depends(access_get)])
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),
                         _: User = Depends(auth_service.get_current_user)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if not contact:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such contact")
    return contact