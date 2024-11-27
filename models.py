from pydantic import BaseModel

class PetBase(BaseModel):
    name: str
    species: str
    age: int
    owner: str

class PetCreate(PetBase):
    pass

class PetResponse(PetBase):
    id: int

    class Config:
        from_attributes = True  # Tell Pydantic to treat SQLAlchemy models as dictionaries
