from sqlalchemy import Column, Integer, String, DateTime, func, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    birthday = Column(Date)
    description = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
