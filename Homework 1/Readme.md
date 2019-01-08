## HomeWork1 BenchMarks

- **Dataset** 
    + [Google Play Store User Reviews](https://www.kaggle.com/lava18/google-play-store-apps)
    + 64.3k rows, 5 columns
    + 7.4 MB  

- **System Configuration**
    + i5-8250U
    + 8 GB RAM
    + OS: Manjaro 18.0.2
    + **PostgreSQL 11.1 on Docker**

- USING python `Psycopg` database adapter
    
    |                    | Try 1 | Try 2 | Try 3 | Try 4 |
    |--------------------|:-----:|:-----:|:-----:|:-----:|
    |One tuple at a time |7.18072|7.29190|6.29063|7.21937|
    |Bulk Load using COPY|0.52465|0.39828|0.50267|0.66483|