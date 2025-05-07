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

INSERT INTO raw_ combined_data
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
CREATE TABLE IF NOT EXISTS combined_data
LIKE raw_combined_data;

INSERT INTO combined_data
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


-- checking inital row count -> 5 860 568d
SELECT COUNT(*)
FROM combined_data; 


-- changing time formats
SELECT *
FROM combined_data
WHERE started_at IS NULL OR ended_at IS NULL;

ALTER TABLE combined_data MODIFY COLUMN started_at datetime NOT NULL;
ALTER TABLE combined_data MODIFY COLUMN ended_at datetime NOT NULL;


-- looking for duplicate rows -> 211 / 422?
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


-- deleting and checking duplicate rows
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


-- indexing columns
ALTER TABLE combined_data 
ADD PRIMARY KEY (ride_id);

ALTER TABLE combined_data
ADD INDEX idx_started_at (started_at),
ADD INDEX idx_ended_at (ended_at),
ADD INDEX idx_member_casual (member_casual);


-- adding new columns and indexing them
ALTER TABLE combined_data
ADD COLUMN ride_length time NOT NULL,
ADD COLUMN ride_length_min double NOT NULL,
ADD COLUMN ride_day varchar(25) NOT NULL,
ADD COLUMN ride_month varchar(25) NOT NULL;

ALTER TABLE combined_data
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


-- excluding rides that shorter than 1 min and longer than 1 day
SELECT count(*) AS to_exclude
FROM combined_data 
WHERE ride_length_min < 1 OR ride_length_min > 1440;

DELETE FROM combined_data
WHERE ride_length_min < 1 OR ride_length_min > 1440;


-- total no. of trips -> 5721391
CREATE VIEW totaltrips AS 
SELECT count(DISTINCT ride_id)
FROM combined_data;


-- total no. of trips per user types
CREATE VIEW totaltrips_perusers AS
SELECT member_casual, count(DISTINCT ride_id) AS total_trips
FROM combined_data
GROUP BY member_casual
ORDER BY total_trips DESC;


-- total no. of trips per bike types
CREATE VIEW totaltrips_perrideables AS 
SELECT member_casual, rideable_type, count(DISTINCT ride_id) AS total_trips
FROM combined_data
GROUP BY member_casual, rideable_type
ORDER BY member_casual, total_trips DESC;


-- total no. of trips per month
CREATE VIEW totaltrips_permonth_ AS
SELECT member_casual, ride_month, count(DISTINCT ride_id) AS total_trips
FROM combined_data
GROUP BY member_casual, ride_month
ORDER BY member_casual, total_trips DESC;


-- total no. of trips per day of week
CREATE VIEW totaltrips_perday AS 
SELECT member_casual, ride_day, count(DISTINCT ride_id) AS total_trips
FROM combined_data
GROUP BY member_casual, ride_day
ORDER BY member_casual, total_trips DESC;


-- total no. of trips per hour of day
CREATE VIEW totaltrips_perhour AS 
SELECT member_casual, EXTRACT(HOUR FROM started_at) AS hours, count(DISTINCT ride_id) AS total_trips
FROM combined_data
GROUP BY member_casual, hours
ORDER BY member_casual, total_trips DESC;


-- avg. length of rides
CREATE VIEW avg_ridelength_perusers AS
SELECT member_casual, avg(ride_length_min) AS avg_ride_length
FROM combined_data
GROUP BY member_casual;


-- avg. length of rides per bike types
CREATE VIEW avg_ridelength_perridables AS
SELECT member_casual, rideable_type, avg(ride_length_min) AS avg_ride_length
FROM combined_data
GROUP BY member_casual, rideable_type
ORDER BY member_casual, avg_ride_length DESC;


-- avg. length of rides per month
CREATE VIEW avg_ridelength_permonth AS
SELECT member_casual, ride_month, avg(ride_length_min) AS avg_ride_length
FROM combined_data
GROUP BY member_casual, ride_month
ORDER BY member_casual, avg_ride_length DESC;


-- avg. length of rides per day of week
CREATE VIEW avg_ridelength_perday AS
SELECT member_casual, ride_day, avg(ride_length_min) AS avg_ride_length
FROM combined_data
GROUP BY member_casual, ride_day
ORDER BY member_casual, avg_ride_length DESC;


-- avg. length of rides per hour of day
CREATE VIEW avg_ridelength_perhour AS
SELECT member_casual, EXTRACT(HOUR FROM started_at) AS hours, avg(ride_length_min) AS avg_ride_length
FROM combined_data
GROUP BY member_casual, hours
ORDER BY member_casual, avg_ride_length DESC;

