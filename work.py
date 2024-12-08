import requests
import pandas as pd
import numpy as np
from datetime import datetime
from faker import Faker
import random

# Parameters
NUM_PETS = 500_000  # Number of pets to generate
CHUNK_SIZE = 10_000  # Chunk size for bulk insert

# API endpoint for fetching the pets data
API_URL = "http://localhost:8000/pets"  # Replace with your actual backend API endpoint


# Fetch function for fetching data in chunks (API request with pagination)
def fetch_pets_in_chunks(api_url, chunk_size=10000):
    all_data = []
    offset = 0  # Start from the first record

    while True:
        # Add pagination parameters (adjust based on API's pagination mechanism)
        paginated_url = f"{api_url}?limit={chunk_size}&offset={offset}"
        print(f"Fetching pets data from {paginated_url}...")

        try:
            response = requests.get(paginated_url)
            response.raise_for_status()
            pets_chunk = response.json()  # Assuming the response is JSON
            if not pets_chunk:  # No more data
                break
            all_data.extend(pets_chunk)
            offset += chunk_size
            print(f"Fetched pets: {offset + 1} to {offset + chunk_size}")

            # Stop if we've reached the desired number of records
            if offset >= NUM_PETS:
                break

        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            break
        except ValueError as e:
            print(f"JSON decode error: {e}")
            break

    return all_data


# Data preprocessing (handling missing values, etc.)
def preprocess_pets_data(pets_data):
    # Create DataFrame
    pets_df = pd.DataFrame(pets_data)

    # Check the shape of the data
    shape = pets_df.shape
    print(f"Shape of pets DataFrame: {shape}")

    # Summary statistics
    print("\nPets DataFrame Information:")
    print(pets_df.info())

    print("\nPets DataFrame Summary Statistics:")
    print(pets_df.describe())

    print("\nPets DataFrame Missing Values:")
    print(pets_df.isnull().sum())

    # Handle missing values with forward fill (only for columns where it's logical, like 'age')
    pets_df['age'].ffill(inplace=True)  # Forward fill for 'age' (assumes a logical progression)
    pets_df['species'].ffill(inplace=True)  # Forward fill for 'species', if needed
    pets_df['owner'].ffill(inplace=True)  # Forward fill for 'owner', if needed

    # Handling duplicates
    pets_df.drop_duplicates(inplace=True)

    # Ensuring 'age' is an integer (if necessary)
    pets_df['age'] = pets_df['age'].astype(int)

    # Final dataset information
    print(f"\nFinal Dataset Information:")
    print(f"Total records in pets dataset: {len(pets_df)}")

    print("\nSample of final dataset:")
    print(pets_df.head())

    print("\nMissing values in final dataset:")
    print(pets_df.isnull().sum())

    # Save the processed data to a CSV file
    output_file = 'processed_pets_data.csv'
    print(f"\nSaving processed data to {output_file}...")
    pets_df.to_csv(output_file, index=False)
    print("Processing complete!")


# Main function
if __name__ == "__main__":
    print("Starting data generation and insertion...")

    # Fetch pets data from the backend API
    print("Fetching pets data...")
    pets_data = fetch_pets_in_chunks(API_URL)

    # Preprocess the fetched data
    preprocess_pets_data(pets_data)

    print("Data processing complete.")
