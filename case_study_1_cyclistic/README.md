# Google Data Analytics course - Case study 1 (Cyclistic)

<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/9bb3c33a-0410-40a1-9c46-f3b34e07eafd">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/9bb3c33a-0410-40a1-9c46-f3b34e07eafd">
  <img alt="Cyclistic bike-share logo. A circle containing a the name of the company and an icon of a person riding a bike." src="https://github.com/user-attachments/assets/9bb3c33a-0410-40a1-9c46-f3b34e07eafd">
 </picture>
</div>

## Introduction
As part of my studies within the Google Data Analytics course, I have successfully completed one of the case studies provided. In order to respond to the business question posed, I analysed the data of a fictional company and created a report on the results.

### About the company
Cyclistic is a fictional bike-sharing company with a network of more than 5800 geotracked bicycles and 600 docking stations. “The bikes can be unlocked from one station and returned to any other station in the system anytime. Until now, Cyclistic’s marketing strategy relied on building general awareness and appealing to broad consumer segments. One approach that helped make these things possible was the flexibility of its pricing plans: single-ride passes, full-day passes, and annual memberships. Customers who purchase single-ride or full-day passes are referred to as casual riders. Customers who purchase annual memberships are Cyclistic members.”

### The scenario
The marketing team’s objective is to increase revenue by converting casual riders into annual members. In order to create a new marketing strategy, it is essential that the team understands the behaviour of the casual riders and members. The team was assigned the task of analysing the historical bike trip data and of identifying trends. 

The question this analysis will address is:

>***“How do annual members and casual riders use Cyclistic bikes differently?”***

### About the data
For the analysis, I used the 2024-year historical bike trip data from the public datasets (accessed 14/05/2025) provided by Motivate International Inc. The datasets were made available under the following license. Due to data-privacy concerns, users’ personally identifiable information was unavailable.


## Data cleaning
*Click [here](https://github.com/kinga-cs/data-analytics-portfolio/blob/main/case_study_1_cyclistic/data_cleaning.sql) to view the full SQL code*

Firstly, I downloaded the 12 CSV files containing the 12 months of data from the 2024 bike trip data, imported them to the database and combined them in a new table (“raw_combined_data”). However, given the size of the dataset – which consists of more than 5 million rows –, I created another table for data cleaning and manipulation (“combined_data”).
```
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

CREATE TABLE IF NOT EXISTS combined_data
LIKE raw_combined_data;

INSERT INTO combined_data
SELECT * FROM raw_combined_data ;
```

Secondly, I made sure the columns holding timestamps (“started_at”, “ended_at”) contained no null values and changed the columns’ format from varchar into datetime. It was necessary since I was unable to import the columns with the correct format, due to repeated errors from the database.
```
SELECT *
FROM combined_data
WHERE started_at IS NULL OR ended_at IS NULL;

ALTER TABLE combined_data MODIFY COLUMN started_at datetime NOT NULL;
ALTER TABLE combined_data MODIFY COLUMN ended_at datetime NOT NULL;
```

The next step was to check if there were any duplicate rows in the combined dataset and to list all of them. Following the confirmation that the 211 entries were indeed duplicates, I removed them and checked the table again for any remaining duplicate rows.
```
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

WITH duplicates AS (
    SELECT *, ROW_NUMBER() OVER (
    	PARTITION BY ride_id ORDER BY started_at, ended_at) AS row_num
    FROM combined_data
)
DELETE FROM combined_data
WHERE ride_id IN (
    SELECT ride_id FROM duplicates WHERE row_num > 1
);
```

In order to improve query performance, I added new columns I would be working with during my analysis, indexed them and set a primary key.
```
ALTER TABLE combined_data
ADD COLUMN ride_length time NOT NULL,
ADD COLUMN ride_length_min double NOT NULL,
ADD COLUMN ride_day varchar(25) NOT NULL,
ADD COLUMN ride_month varchar(25) NOT NULL;

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
```

The newly added columns were then populated with calculation results.
```
UPDATE combined_data
SET ride_length = sec_to_time(timestampdiff(SECOND, started_at, ended_at));

UPDATE combined_data
SET ride_length_min = (timestampdiff(SECOND, started_at, ended_at) / 60);

UPDATE combined_data
SET ride_day = dayname(started_at);

UPDATE combined_data
SET ride_month = monthname(started_at);
```

Finally, I excluded rides that are shorter than 1 minute and longer than 24 hour. They, supposedly, were either data recording or human errors (e.g. user accidentally starting a ride or forgetting to end the ride).
```
SELECT count(*) AS to_exclude
FROM combined_data 
WHERE ride_length_min < 1 OR ride_length_min > 1440;

DELETE FROM combined_data
WHERE ride_length_min < 1 OR ride_length_min > 1440;
```

As a result, the final row count of the dataset was reduced by 139 177 rows (from 5 860 568 to 5 721 391).


<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/7351239f-cff3-4e47-b10c-ef30903b3021">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/7351239f-cff3-4e47-b10c-ef30903b3021">
  <img alt="Figure 1" src="https://github.com/user-attachments/assets/7351239f-cff3-4e47-b10c-ef30903b3021">
 </picture>
</div>
<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/f9a3c8dd-af0e-4d2d-865b-b785dd9f0629">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/f9a3c8dd-af0e-4d2d-865b-b785dd9f0629">
  <img alt="Figure 2" src="https://github.com/user-attachments/assets/f9a3c8dd-af0e-4d2d-865b-b785dd9f0629">
 </picture>
</div>
<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/2323d4de-7efd-4b87-988e-b44cdbf5a341">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/2323d4de-7efd-4b87-988e-b44cdbf5a341">
  <img alt="Figure 3" src="https://github.com/user-attachments/assets/2323d4de-7efd-4b87-988e-b44cdbf5a341">
 </picture>
</div>
<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/1af7034a-5ad6-44d1-93d5-a0746dce5c51">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/1af7034a-5ad6-44d1-93d5-a0746dce5c51">
  <img alt="Figure 4" src="https://github.com/user-attachments/assets/1af7034a-5ad6-44d1-93d5-a0746dce5c51">
 </picture>
</div>
<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/c80c0bef-dd43-4d6b-8729-50b8e9941be0">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/c80c0bef-dd43-4d6b-8729-50b8e9941be0">
  <img alt="Figure 5" src="https://github.com/user-attachments/assets/c80c0bef-dd43-4d6b-8729-50b8e9941be0">
 </picture>
</div>
<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/0f2693d3-0a96-47bd-b63a-a832efcc0d91">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/0f2693d3-0a96-47bd-b63a-a832efcc0d91">
  <img alt="Figure 6" src="https://github.com/user-attachments/assets/0f2693d3-0a96-47bd-b63a-a832efcc0d91">
 </picture>
</div>
<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/f3a40872-1249-4bfa-94b5-dbb835f334ca">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/f3a40872-1249-4bfa-94b5-dbb835f334ca">
  <img alt="Figure 7" src="https://github.com/user-attachments/assets/f3a40872-1249-4bfa-94b5-dbb835f334ca">
 </picture>
</div>
<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/b41c6835-338f-4d58-85f3-1f0e199c86c0">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/b41c6835-338f-4d58-85f3-1f0e199c86c0">
  <img alt="Figure 8" src="https://github.com/user-attachments/assets/b41c6835-338f-4d58-85f3-1f0e199c86c0">
 </picture>
</div>
<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/a4302590-4201-4ae3-a74f-faf5400fdb52">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/a4302590-4201-4ae3-a74f-faf5400fdb52">
  <img alt="Figure 9" src="https://github.com/user-attachments/assets/a4302590-4201-4ae3-a74f-faf5400fdb52">
 </picture>
</div>
<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/0418743a-46be-4ec1-ad21-65affca56736">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/0418743a-46be-4ec1-ad21-65affca56736">
  <img alt="Figure 10" src="https://github.com/user-attachments/assets/0418743a-46be-4ec1-ad21-65affca56736">
 </picture>
</div>
