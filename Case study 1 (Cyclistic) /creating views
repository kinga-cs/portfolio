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
