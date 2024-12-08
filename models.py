from sqlalchemy import Column, Integer, String
from database import Base


from pydantic import BaseModel

class Pet(Base):
    __tablename__ = 'pets'  # The name of the table in the database

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    species = Column(String)
    age = Column(Integer)
    owner = Column(String)

# Pydantic models for request/response
class PetBase(BaseModel):
    name: str
    species: str
    age: int
    owner: str

# models.py
from pydantic import BaseModel
from pydantic import BaseModel

class PetCreate(BaseModel):
    name: str
    species: str  # Ensure species is defined here
    age: int
    owner: str



class PetResponse(PetBase):
    id: int

    class Config:
        orm_mode = True  # Tells Pydantic to treat SQLAlchemy models as dictionaries
