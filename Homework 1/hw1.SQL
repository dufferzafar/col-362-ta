--Creating Custom Data Type--

CREATE TYPE Sentiment AS ENUM ('Positive', 'Negative', 'Neutral', 'nan');

--TO MEASURE PERFORMANCE--
EXPLAIN ANALYZE --Not sure--
\timing --This works--

--Creating Table--

CREATE TABLE playstore(
	appid SERIAL PRIMARY KEY,
	app_name varchar,
	review varchar,
	senti Sentiment,
	polarity REAL,
	subjectivity double precision
);

--Inserting into Table--
--Use single quotes for strings--

INSERT INTO playstore
(app_name, review, senti, polarity, subjectivity)
VALUES
('test','wtf','Neutral',1.0,456);

--Bulk Loading Tuples--
COPY playstore(app_name, review, senti, polarity, subjectivity) FROM '/data/playstore-reviews.csv' DELIMITER ',' CSV HEADER;
