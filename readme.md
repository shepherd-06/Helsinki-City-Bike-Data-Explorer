# Helsinki City Bike Data Explorer

This project focuses on processing and analyzing city bike trip data for eventual visualization in a `Tableau` or `Power BI` dashboard. We handle `data extraction`, `transformation`, and `loading (ETL)` from `CSV` files into a `PostgreSQL` database, with a goal to `visualize` insights after pre-processing.

## Project Overview

1. **Data Source**: CSV files containing city bike trips from `April to October` for the years `2021-2023`.
2. **Data Cleaning and ETL**: Python script for data cleaning and bulk insertion into a PostgreSQL database.
3. **Final Dashboard**: Data will be visualized in a `Tableau` or `Power BI` dashboard after pre-processing with Python.

---

## Requirements

- **Python 3.7+**
- **PostgreSQL**
- **Python Libraries**: Install required packages:
  
  ```bash
  pip install -r requirements.txt
  ```

## Database Schema

The PostgreSQL database includes a table `city_bike_trips` with the following schema:

```SQL
CREATE TABLE city_bike_trips (
    id SERIAL PRIMARY KEY,
    departure TIMESTAMP NOT NULL,
    return TIMESTAMP NOT NULL,
    departure_station_id INTEGER NOT NULL,
    departure_station_name VARCHAR(255) NOT NULL,
    return_station_id INTEGER NOT NULL,
    return_station_name VARCHAR(255) NOT NULL,
    covered_distance FLOAT NOT NULL,
    duration INTEGER NOT NULL
);
```

### Schema Details

- `departure and return`: Timestamps for trip start and end
- `departure_station_id`, `return_station_id`: IDs of the departure and return stations
- `departure_station_name`, `return_station_name`: Names of the departure and return stations
- `covered_distance`: Trip distance in meters
- `duration`: Trip duration in seconds

## Python ETL Script

The Python script reads and cleans each CSV file, then loads it into the PostgreSQL database in bulk. The script includes logging, error handling, and checkpointing to allow resuming from the last processed file in case of interruption.

### Configuration

1. **Database URI**: Replace with your database credentials in the script:

```python
DATABASE_URI = 'postgresql://username:password@localhost:5432/your_database'
```

2. **Data Folder**: Specify the folder path containing the CSV files:

```python
data_folder = 'data/'
```

### Script Usage

Run the script to process and load data into PostgreSQL:

```bash
python insert_data_script.py
```

#### Script Features

- Data Cleaning: Converts timestamps and removes rows with missing critical values.
- Bulk Insertion: Uses pandas.to_sql for efficient insertion with SQLAlchemy.
- Logging: Logs steps and errors to data_import.log.
- Checkpointing: Creates a .checkpoint file after each successful file, allowing restarts from the last processed file.

## Logging and Error Handling

The script logs each step to `data_import.log`, including:

- File processing start and end
- Data cleaning steps
- Bulk insertion success and errors

If a failure occurs, the script stops and can resume from the last unprocessed file due to checkpoint files.

## Final Dashboard

After completing data pre-processing, the data will be visualized in a Tableau or Power BI dashboard, providing insights into city bike trip patterns. The dashboard will leverage PostgreSQL as the data source to explore trends, station popularity, trip durations, and distances over time.

## Data Clarification

The Origin–Destination (OD) data of city bike stations includes all journeys made by city bikes in Helsinki and Espoo. The data provides comprehensive details about each trip, including:

- Origin and destination station
- Start and end times
- Distance traveled (in meters)
- Duration of each journey (in seconds)

Data is available from the 2016 season onward and can be accessed by month (as CSV files) or for the entire season (as ZIP files). The data is owned by City Bike Finland.

**Data collected from**: [HSL Open Data](https://www.hsl.fi/en/hsl/open-data)
