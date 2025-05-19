-- combining all 12 tables
CREATE TABLE IF NOT EXISTS raw_combined_data (
ride_id varchar(225) NOT NULL,
rideable_type varchar(225) NOT NULL,
started_at varchar(225) NOT NULL,
ended_at varchar(225) NOT NULL,
start_station_name varchar(225) NULL,
start_station_id varchar(225) NULL,
end_station_name varchar(225) NULL,
end_station_id varchar(225) NULL,
start_lat double NULL,
start_lng double NULL,
end_lat double NULL,
end_lng double NULL,
member_casual varchar(225) NOT NULL
);

INSERT INTO raw_combined_data
(
SELECT * FROM raw_jan2024
UNION ALL
SELECT * FROM raw_feb2024
UNION ALL
SELECT * FROM raw_mar2024
UNION ALL
SELECT * FROM raw_apr2024
UNION ALL
SELECT * FROM raw_may2024
UNION ALL
SELECT * FROM raw_jun2024
UNION ALL
SELECT * FROM raw_jul2024
UNION ALL
SELECT * FROM raw_aug2024
UNION ALL
SELECT * FROM raw_sep2024
UNION ALL
SELECT * FROM raw_oct2024
UNION ALL
SELECT * FROM raw_nov2024
UNION ALL
SELECT * FROM raw_dec2024
);


-- creating a table for data cleaning and manipulation
CREATE TABLE IF NOT EXISTS test
LIKE raw_combined_data;

INSERT INTO test
SELECT * FROM raw_combined_data;


-- inital row count -> 5 860 568
SELECT COUNT(*)
FROM combined_data; 


-- changing time formats
SELECT *
FROM combined_data
WHERE started_at IS NULL OR ended_at IS NULL;

ALTER TABLE combined_data MODIFY COLUMN started_at datetime NOT NULL;
ALTER TABLE combined_data MODIFY COLUMN ended_at datetime NOT NULL;


-- checking the number of duplicate rows, if any -> 211
SELECT count(ride_id) - count(DISTINCT ride_id) AS duplicate_rows
FROM combined_data;


-- seeing which rows are the duplicates
WITH duplicates AS (
    SELECT *, ROW_NUMBER() OVER (
    	PARTITION BY ride_id ORDER BY started_at, ended_at) AS row_num
    FROM combined_data
)
SELECT *
FROM duplicates
WHERE row_num > 1;


-- deleting and checking duplicate rows again
WITH duplicates AS (
    SELECT *, ROW_NUMBER() OVER (
    	PARTITION BY ride_id ORDER BY started_at, ended_at) AS row_num
    FROM combined_data
)
DELETE FROM combined_data
WHERE ride_id IN (
    SELECT ride_id FROM duplicates WHERE row_num > 1
);

SELECT count(ride_id) - count(DISTINCT ride_id) AS duplicate_rows
FROM combined_data;

WITH duplicates AS (
    SELECT *, ROW_NUMBER() OVER (
    	PARTITION BY ride_id ORDER BY started_at, ended_at) AS row_num
    FROM combined_data
)
SELECT *
FROM duplicates
WHERE row_num > 1;


-- adding new columns and indexing them
ALTER TABLE combined_data
ADD COLUMN ride_length time NOT NULL,
ADD COLUMN ride_length_min double NOT NULL,
ADD COLUMN ride_day varchar(25) NOT NULL,
ADD COLUMN ride_month varchar(25) NOT NULL;

-- indexing columns
ALTER TABLE combined_data 
ADD PRIMARY KEY (ride_id);

ALTER TABLE combined_data
ADD INDEX idx_started_at (started_at),
ADD INDEX idx_ended_at (ended_at),
ADD INDEX idx_member_casual (member_casual),
ADD INDEX idx_ride_length (ride_length),
ADD INDEX idx_ride_length_min (ride_length_min),
ADD INDEX idx_ride_day (ride_day),
ADD INDEX idx_ride_month (ride_month);


-- inserting data into new columns
UPDATE combined_data
SET ride_length = sec_to_time(timestampdiff(SECOND, started_at, ended_at));

UPDATE combined_data
SET ride_length_min = (timestampdiff(SECOND, started_at, ended_at) / 60);

UPDATE combined_data
SET ride_day = dayname(started_at);

UPDATE combined_data
SET ride_month = monthname(started_at);


-- excluding rides shorter than 1 min and longer than 1 day
SELECT count(*) AS to_exclude
FROM combined_data 
WHERE ride_length_min < 1 OR ride_length_min > 1440;

DELETE FROM combined_data
WHERE ride_length_min < 1 OR ride_length_min > 1440;
