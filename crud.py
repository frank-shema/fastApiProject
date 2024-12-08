from sqlalchemy.orm import Session
import models

# Create a new pet
def create_pet(db: Session, pet: models.PetCreate):
    db_pet = models.Pet(name=pet.name, species=pet.species, age=pet.age, owner=pet.owner)
    db.add(db_pet)
    db.commit()
    db.refresh(db_pet)
    return db_pet

# Get all pets
def get_pets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Pet).offset(skip).limit(limit).all()

# Get a pet by ID
def get_pet(db: Session, pet_id: int):
    return db.query(models.Pet).filter(models.Pet.id == pet_id).first()

# Update a pet by ID
def update_pet(db: Session, pet_id: int, pet: models.PetCreate):
    db_pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if db_pet:
        db_pet.name = pet.name
        db_pet.species = pet.species
        db_pet.age = pet.age
        db_pet.owner = pet.owner
        db.commit()
        db.refresh(db_pet)
        return db_pet
    return None

# Delete a pet by ID
def delete_pet(db: Session, pet_id: int):
    db_pet = db.query(models.Pet).filter(models.Pet.id == pet_id).first()
    if db_pet:
        db.delete(db_pet)
        db.commit()
        return db_pet
    return None
