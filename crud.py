from sqlalchemy.orm import Session
from models import Item
from schemas import AddressCreate, AddressUpdate,  AddressBase
from typing import Union
from math import sin, cos, sqrt, atan2, radians


#List all the Addresses max limit 50
def list_details(db: Session, limit: int = 50):
    return db.query(Item).limit(limit).all()

#Check if Address already exists or BOTH latitude and longitude already exist
def get_item_by_address(db: Session, address_new: str, latitude_new: str, longitude_new:str):
    if db.query(Item).filter(Item.address == address_new).first() and db.query(Item).filter(Item.latitude == latitude_new).first() and db.query(Item).filter(Item.longitude == longitude_new).first():
        return 0
    else:
        return 1

#Get details by id
def get_details(db: Session, id: int):
    return db.query(Item).get(id)

#Find nearest Addresses from a given (lat,long) by using Haversine's formula
#https://en.wikipedia.org/wiki/Haversine_formula
#https://community.esri.com/t5/coordinate-reference-systems-blog/distance-on-a-sphere-the-haversine-formula/ba-p/902128

def get_address_by_distance(db: Session, distance: str, latitude:str, longitude:str):
    data = []
    list_lat = [float(id) for id, in db.query(Item.latitude).all()]
    list_long = [float(id) for id, in db.query(Item.longitude).all()]

    # Radius of earth in km
    R = 6373.0

    for i in range(len(list_lat)):
        dellong = float(longitude) - list_long[i]
        dellat = float(latitude) - list_lat[i]

        a = sin(dellat / 2)**2 + cos(float(latitude)) * cos(list_lat[i]) * sin(dellong / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        caldistance = R * c

        if caldistance <= float(distance):
            # print(list_lat[i],"-------------")
            # print(list_long[i])
            data = db.query(Item).filter(Item.latitude == list_lat[i]).all()
    return data

#Create a new Address
def create_item(db: Session, data: AddressCreate):
    db_item = Item(**data.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

#Delete an Address
def drop_item(db: Session, address_id: int):
    db.query(Item).filter(Item.id == address_id).delete()
    db.commit()
    return None

#Update an existing Address
def update_address(db: Session, address: Union[int, Item], data: AddressUpdate):
    if isinstance(address, int):
        address = get_details(db, address)
    for key, value in data:
        setattr(address, key, value)
    db.commit()
    return address