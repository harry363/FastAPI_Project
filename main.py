from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

import models, crud, schemas
from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/DisplayAllAddressDetails", response_model=List[schemas.Item])
async def display_address_details(limit: int = 50, db: Session = Depends(get_db)):
    details = crud.list_details(db, limit)
    return details


# @app.get("/GetDetailsByAddress/{address_id}", response_model=schemas.Item)
# def items_action_retrieve(address_id: str, db: Session = Depends(get_db)):
#     details = crud.get_item(db, address_id)
#     if details is None:
#         raise HTTPException(status_code=400, detail="Address does not exist in database!")
#     return details

#Get All Address Details within a certain radius from given (lat,long)
@app.get("/GetDetailsByDistance/{distance}/{latitude}/{longitude}", response_model=List[schemas.Item])
async def address_get_distance(distance: str, latitude: str, longitude: str, limit: int = 50, db: Session = Depends(get_db)):
    details = crud.get_address_by_distance(db, distance, latitude, longitude)
    return details

#Create a new Address entry, Raise error if address, lat and long already exist
@app.post("/PostAddressDetails", response_model=schemas.Item)
async def create_address_details(data: schemas.AddressCreate, db: Session = Depends(get_db)):
    if not crud.get_item_by_address(db, data.address, data.latitude, data.longitude):
        raise HTTPException(status_code=400, detail="Address, Latitude and Longitude already exist in database!")
    # if not crud.get_item_by_latlong(db, data.latitude, data.longitude):
    #     raise HTTPException(status_code=400, detail="Latitude and Longitude already exist in database!")
    details = crud.create_item(db, data)
    return details

#Change Address details by Address ID
@app.put("/PutAddress/{address_id}", response_model=schemas.Item)
def change_address_details(address_id: int, data: schemas.AddressUpdate,  db: Session = Depends(get_db)):
    details = crud.update_address(db, address_id, data)
    if details is None:
        raise HTTPException(status_code=400, detail="No such address ID found")
    return details

#Delete Address Details by Address ID
@app.delete("/DeleteAddress/{address_id}", status_code=204)
def delete_address_details(address_id: int,  db: Session = Depends(get_db)):
    crud.drop_item(db, address_id)
    return None