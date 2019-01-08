import psycopg2
import time
import csv
from tqdm import tqdm

# Creating Connection to the server
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="docker",
    host="127.0.0.1",
    port="5432"
)

# Cursor that executes queries
cur = conn.cursor()


# Drop Old Table and Create New Table

create_table = '''
    DROP TABLE playstore;
    CREATE TABLE playstore(
        appid SERIAL PRIMARY KEY,
        app_name varchar,
        review varchar,
        senti Sentiment,
        polarity REAL,
        subjectivity double precision
    );
    '''
cur.execute(create_table)


# One by one insert for each tuple in database
query = '''
    INSERT INTO playstore
    (app_name, review, senti, polarity, subjectivity)
    VALUES
    (%s,%s,%s,%s,%s);
    '''

t_time = 0
csv_reader = csv.reader(open("data/playstore-reviews.csv", "r"), delimiter=',')
next(csv_reader)

for row in tqdm(csv_reader, ascii=True):
    start_time = time.time()
    cur.execute(query, row)
    t_time += time.time() - start_time

print("Time Taken Inserting Each tuple one at a time:", t_time)

# Delete all entries for fresh comparison
cur.execute('DELETE FROM playstore;')

# Bulk Load

query = "COPY playstore(app_name, review, senti, polarity, subjectivity) FROM '/data/playstore-reviews.csv' DELIMITER ',' CSV HEADER;"

start_time = time.time()
cur.execute(query)
t_time = time.time() - start_time

print("Time Taken Using Bulk Load:", t_time)

# Persistent Changes to the DB
conn.commit()

# Close the connection
conn.close()
