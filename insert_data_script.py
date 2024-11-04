import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import logging

# Configure logging
logging.basicConfig(filename='data_import.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Database configuration
DATABASE_URI = 'postgresql://postgres:postgres@localhost:5432/550_2'
engine = create_engine(DATABASE_URI)

# Folder paths and file pattern
data_folder = 'data/'  # Update this path to your data folder

def clean_data(df):
    """Clean the data to prepare it for insertion."""
    logging.info("Cleaning data")
    
    # Ensure timestamps are properly formatted
    df['Departure'] = pd.to_datetime(df['Departure'], errors='coerce')
    df['Return'] = pd.to_datetime(df['Return'], errors='coerce')
    
    # Drop rows with null values in critical columns
    df.dropna(subset=['Departure', 'Return', 'Departure station id', 
                      'Return station id', 'Covered distance (m)', 'Duration (sec.)'], inplace=True)
    
    # Rename columns to match database table column names
    df.rename(columns={
        'Departure': 'departure',
        'Return': 'return',
        'Departure station id': 'departure_station_id',
        'Departure station name': 'departure_station_name',
        'Return station id': 'return_station_id',
        'Return station name': 'return_station_name',
        'Covered distance (m)': 'covered_distance',
        'Duration (sec.)': 'duration'
    }, inplace=True)
    
    logging.info("Data cleaned successfully")
    return df

def insert_data(df, table_name):
    """Insert data into the PostgreSQL database using bulk insert."""
    try:
        logging.info("Starting bulk insert into database")
        df.to_sql(table_name, engine, if_exists='append', index=False, method='multi', chunksize=500)
        logging.info("Bulk insert completed successfully")
    except SQLAlchemyError as e:
        logging.error(f"Error during data insertion: {e}")
        raise  # Re-raise to handle the error outside

def process_file(file_path):
    """Process each file and handle errors to allow resuming if needed."""
    try:
        logging.info(f"Processing file {file_path}")
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Clean the data
        df = clean_data(df)
        
        # Insert data into database
        insert_data(df, 'city_bike_trips')
        
        logging.info(f"File {file_path} processed successfully")
    except Exception as e:
        logging.error(f"Failed to process file {file_path}: {e}")
        raise  # Raise to handle restart

def main():
    # Iterate over each file in the folder
    for year in range(2021, 2024):  # Loop through 2021, 2022, and 2023
        folder_path = os.path.join(data_folder, f'od-trips-{year}')
        
        for month in range(4, 11):  # Loop from April (4) to October (10)
            file_name = f"{year}-{str(month).zfill(2)}.csv"
            file_path = os.path.join(folder_path, file_name)
            
            # Check if file processing has been completed
            checkpoint_file = f"checkpoints/{file_name}.checkpoint"
            if os.path.exists(checkpoint_file):
                logging.info(f"Skipping file {file_path} (already processed)")
                continue  # Skip files that have already been processed
            
            try:
                process_file(file_path)
                
                # Create checkpoint after successful processing
                with open(checkpoint_file, 'w') as f:
                    f.write("Processed")
                logging.info(f"Checkpoint created for file {file_name}")
            
            except Exception as e:
                logging.error(f"Error processing file {file_name}. Restarting from this file.")
                break  # Stop processing if a file fails, allowing restart from this point

if __name__ == "__main__":
    main()
