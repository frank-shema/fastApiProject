from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import crud
import models
import database

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new pet
@app.post("/pets/", response_model=models.PetResponse)
def create_pet(pet: models.PetCreate, db: Session = Depends(get_db)):
    return crud.create_pet(db=db, pet=pet)

# Get all pets
@app.get("/pets/", response_model=List[models.PetResponse])
def get_all_pets(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_pets(db=db, skip=skip, limit=limit)

# Get a pet by ID
@app.get("/pets/{pet_id}", response_model=models.PetResponse)
def get_pet(pet_id: int, db: Session = Depends(get_db)):
    pet = crud.get_pet(db=db, pet_id=pet_id)
    if pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return pet

# Update a pet by ID
@app.put("/pets/{pet_id}", response_model=models.PetResponse)
def update_pet(pet_id: int, pet: models.PetCreate, db: Session = Depends(get_db)):
    updated_pet = crud.update_pet(db=db, pet_id=pet_id, pet=pet)
    if updated_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return updated_pet

# Delete a pet by ID
@app.delete("/pets/{pet_id}", response_model=models.PetResponse)
def delete_pet(pet_id: int, db: Session = Depends(get_db)):
    deleted_pet = crud.delete_pet(db=db, pet_id=pet_id)
    if deleted_pet is None:
        raise HTTPException(status_code=404, detail="Pet not found")
    return deleted_pet
