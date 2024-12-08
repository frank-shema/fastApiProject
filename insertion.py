from faker import Faker
import random
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

# Database connection
DATABASE_URL = "postgresql://postgres:db_passcode@localhost/petsdata"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


# New PetCreate model
class PetCreate(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    species = Column(String, index=True)
    age = Column(Integer)
    owner = Column(String, index=True)


# Create the tables
Base.metadata.create_all(engine)

# Faker instance
fake = Faker()

# Parameters
NUM_PETS = 500_000  # Number of pets to generate
CHUNK_SIZE = 10_000  # Chunk size for bulk insert


# Insert pets in chunks
def insert_pets(num_pets):
    for start in range(0, num_pets, CHUNK_SIZE):
        end = min(start + CHUNK_SIZE, num_pets)
        pets = [
            PetCreate(
                name=fake.first_name(),
                species=random.choice(["Dog", "Cat", "Bird", "Rabbit", "Fish"]),
                age=random.randint(1, 15),
                owner=fake.name()
            )
            for i in range(end - start)
        ]

        try:
            session.bulk_save_objects(pets)
            session.commit()
            print(f"Inserted pets: {start + 1} to {end}")
        except Exception as e:
            session.rollback()
            print(f"Error inserting pets {start + 1} to {end}: {e}")


# Main function
if __name__ == "__main__":
    print("Starting data generation and insertion...")

    # Insert pets
    print("Inserting pets...")
    insert_pets(NUM_PETS)

    print("Data insertion complete.")
