from typing import Optional
from pydantic import BaseModel


class AddressBase(BaseModel):
    address: str
    latitude: str
    longitude: str


class AddressCreate(AddressBase):
    pass


class AddressUpdate(AddressBase):
    pass


class Item(AddressBase):
    id: int

    # Pydantic can be controlled via the Config class on a model
    # Supports models that map to ORM for this orm_mode must be true

    class Config:
        orm_mode = True
