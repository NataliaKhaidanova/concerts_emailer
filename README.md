# concerts_emailer

-- STAGE --
CREATE TABLE stage.concerts_emailer (
	scrape_date date,
	artist TEXT,
	concert_date date,
	venue TEXT
);

SELECT * FROM stage.concerts_emailer;
