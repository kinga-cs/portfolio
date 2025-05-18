# Google Data Analytics course - Case study 1 (Cyclistic)

<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/9bb3c33a-0410-40a1-9c46-f3b34e07eafd">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/9bb3c33a-0410-40a1-9c46-f3b34e07eafd">
  <img alt="Cyclistic bike-share logo. A circle containing the name of the company and an icon of a person riding a bike." src="https://github.com/user-attachments/assets/9bb3c33a-0410-40a1-9c46-f3b34e07eafd">
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
*(Click [here](https://github.com/kinga-cs/data-analytics-portfolio/blob/main/case_study_1_cyclistic/data_cleaning.sql) for the full SQL code)*

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

## Analysing and sharing insights

In the current section of the case study, I will share the insights of my analysis with the help of various charts, as well as, address the previously posed question (“How do annual members and casual riders use Cyclistic bikes differently?”).

<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/34b40203-f02f-4fce-98f4-8289a358fd5d">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/34b40203-f02f-4fce-98f4-8289a358fd5d">
  <img alt="Figure 1" src="https://github.com/user-attachments/assets/34b40203-f02f-4fce-98f4-8289a358fd5d">
 </picture>
</div>
In 2024, annual members used the bike-sharing service more frequently ...

<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/77e15d94-637c-4b95-8f35-d545f7afd2d0">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/77e15d94-637c-4b95-8f35-d545f7afd2d0">
  <img alt="Figure 6" src="https://github.com/user-attachments/assets/77e15d94-637c-4b95-8f35-d545f7afd2d0">
 </picture>
</div>
... while casual riders were more likely to take longer bike trips.

<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/50952908-ab7e-4aad-836b-faba90dd1845">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/50952908-ab7e-4aad-836b-faba90dd1845">
  <img alt="Figure 2" src="https://github.com/user-attachments/assets/50952908-ab7e-4aad-836b-faba90dd1845">
 </picture>
</div>
In general, users preferred electric bikes as opposed to classic bikes and electric scooters.

<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/d3cb0b30-34c5-4c2a-ab7a-c1b9c49c6757">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/d3cb0b30-34c5-4c2a-ab7a-c1b9c49c6757">
  <img alt="Figure 7" src="https://github.com/user-attachments/assets/d3cb0b30-34c5-4c2a-ab7a-c1b9c49c6757">
 </picture>
</div>
On average, casual riders rented the classic bike for the longest periods of time.

<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/4ac4bfa7-8d9a-4a64-a3aa-a6cf24239a10">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/4ac4bfa7-8d9a-4a64-a3aa-a6cf24239a10">
  <img alt="Figure 3" src="https://github.com/user-attachments/assets/4ac4bfa7-8d9a-4a64-a3aa-a6cf24239a10">
 </picture>
</div>
Contrary to my preliminary assumption, the month with the highest number of trips was September and not one of the summer months. Following a research for the cause, it can be safely assumed that September's high number was due to the Bike the Drive fundraiser event that took place on the 1st September 2024. For the event, a 30-mile (~48,3 km) long road was closed to traffic for the bikers in Chicago.

<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/59011289-e0c6-43f4-adb1-2b7978298adf">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/59011289-e0c6-43f4-adb1-2b7978298adf">
  <img alt="Figure 8" src="https://github.com/user-attachments/assets/59011289-e0c6-43f4-adb1-2b7978298adf">
 </picture>
</div>
As one would expect, the longest rides on average occured between during the months of late spring, early and mid-summer.

<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/e791bc0c-7bd9-465d-a913-0008a4a1d60e">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/e791bc0c-7bd9-465d-a913-0008a4a1d60e">
  <img alt="Figure 4" src="https://github.com/user-attachments/assets/e791bc0c-7bd9-465d-a913-0008a4a1d60e">
 </picture>
</div>
Annual members used the service mostly on the weekdays, while casual riders rented bikes during the weekends ...

<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/5a71f352-fb66-48cc-a4c6-09a622bd2464">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/5a71f352-fb66-48cc-a4c6-09a622bd2464">
  <img alt="Figure 9" src="https://github.com/user-attachments/assets/5a71f352-fb66-48cc-a4c6-09a622bd2464">
 </picture>
</div>
... however, both annual members and casual riders took longer trips during the weekends.

<div align="center">
 <picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://github.com/user-attachments/assets/806afa1f-06f5-4f73-a189-ee62e5dcb290">
  <source media="(prefers-color-scheme: light)" srcset="https://github.com/user-attachments/assets/806afa1f-06f5-4f73-a189-ee62e5dcb290">
  <img alt="Figure 5" src="https://github.com/user-attachments/assets/806afa1f-06f5-4f73-a189-ee62e5dcb290">
 </picture>
</div>
The highest numbers of bike rents occured between 5 and 6pm. Up to this time of the day, casual riders' trip numbers grew steadily throughout the day. However, a further inscrease in the annual members' trip numbers can be observed, between 8 and 9am. These suggest that on the one hand, annual members used the service as a means of transport to and from work. On the other hand, casual riders most likely were tourists who discovered the city of Chicago on rented bikes.
