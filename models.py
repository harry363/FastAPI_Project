from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class Item(Base):
    __tablename__ = "addressbook"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    address = Column(String, index=True, nullable=False)

    #String to store more precise location
    latitude = Column(String, index=True, nullable=False)
    longitude = Column(String, index=True, nullable=False)