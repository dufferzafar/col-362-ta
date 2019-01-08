## postgreSQL

- Pull Docker

    `sudo dokcer pull postgres`

- Start Docker Image
    
    `make start-postgres` 

    This runs the follwoing command:

    ```bash
    sudo docker run --rm  --name pg-docker -e POSTGRES_PASSWORD=docker \
    -d -p 5432:5432 -v $$HOME/docker/volumes/postgres:/var/lib/postgresql/data \
    -v $$(realpath data):/data postgres

    ```

    Above command is explained [here.](https://hackernoon.com/dont-install-postgres-docker-pull-postgres-bee20e200198)

- Enter Bash of Docker Image

    `make postgres-bash`

    This runs the following command:
        
    ```bash
    sudo docker exec -it $$(sudo docker ps -a -q) bash`
    ```

- Start postgreSQL shell

    `psql -U postgres`

    Type `\connninfo` to check connection to PostgreSQL DB
    
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