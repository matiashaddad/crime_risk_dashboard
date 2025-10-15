CREATE TABLE IF NOT EXISTS crime_data (
    rank INTEGER,
    city TEXT,
    country TEXT,
    crime_index REAL,
    safety_index REAL,
    PRIMARY KEY (city, country)
);
