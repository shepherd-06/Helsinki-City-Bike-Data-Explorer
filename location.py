import csv
import psycopg2

# Database connection parameters
DB_NAME = "550_2"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "localhost"

# File paths
files = [
    "data/Helsingin_ja_Espoon.csv",
    "data/Vantaan.csv"
]

# Function to read and insert station data
def process_csv_and_insert(file_path, conn):
    with open(file_path, encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # Map columns from the file to the table fields
            station_id = int(row["ID"])
            name = row["Name"]
            city = row["Kaupunki"]
            latitude = float(row["x"])
            longitude = float(row["y"])

            # Insert into the database
            with conn.cursor() as cur:
                try:
                    cur.execute(
                        """
                        INSERT INTO Station (id, name, city, latitude, longitude)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (id) DO NOTHING
                        """,
                        (station_id, name, city, latitude, longitude)
                    )
                except Exception as e:
                    print(f"Error inserting station {station_id}: {e}")
        conn.commit()

# Main script
if __name__ == "__main__":
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST
    )
    
    # Process each CSV file
    for file in files:
        process_csv_and_insert(file, conn)
        print(f"Processed {file}")

    # Close the database connection
    conn.close()
    print("All files processed and database updated!")
