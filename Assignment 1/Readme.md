
# Assignment 1


## Server Work

* Passwordless
* Upgrade
    - `apt-get purge libappstream3`
* Install
    - tmux, ranger, lynx
    - Proxy script

* Install VPL Jail Server
    - Download Tarballs
        + `wget http://vpl.dis.ulpgc.es/releases/vpl-jail-system-2.2.3.tar.gz1`
        + `tar -xvf vpl-jail-system-2.2.3.tar.gz`
    - Config file
        + In `vpl-jail-system.conf` make the following changes
            * `PORT=80` --> `PORT=8080`
            * `FIREWALL=2` --> `FIREWALL=0`
    - Test working?
        + Moodle dummy activity

### Postgres

    * Latest, v11.0
        + https://websiteforstudents.com/how-to-install-postgresql-11-on-ubuntu-16-04-18-04-servers/
        + Had to run the internet proxy script

    * Setup
        + `postgresql.conf`
            * `listen_address`
        + `pg_hba.conf`
            * `trust, 0.0.0.0/0`

    * Load HW 1 Data
    * Test working
        + Run SQL queries etc.

    * VPL + Postgres

        - Frontend / Activity
            + SQL
            + HW1 SQL

        - Backend / VPL
            + evaluate.sh
                * bash script
                * run .sql via psql
                * can output

    * Setting up 3rd server

    * Setting up roles and database, on `vpl1`

        ```sql
        DROP DATABASE vpl_db;
        DROP ROLE vpl_user;

        CREATE ROLE vpl_user WITH LOGIN;
        CREATE DATABASE vpl_db;

        -- Connect to vpl_db
        -- CREATE SCHEMA vpl_schema;

        -- Connect to vpl_db
        -- CREATE TABLES
        \c vpl_db
        \i meta/schema.sql

        REVOKE ALL ON SCHEMA public FROM public;
        GRANT ALL ON SCHEMA public TO postgres;

        REVOKE ALL ON DATABASE vpl_db FROM public;
        GRANT ALL ON DATABASE vpl_db TO postgres;
        
        GRANT CONNECT ON DATABASE vpl_db TO vpl_user;
        GRANT SELECT ON Paper, Author, PaperByAuthors, Citation, Venue TO vpl_user;

        GRANT USAGE ON schema public TO vpl_user;
        GRANT CREATE ON schema public TO vpl_user;
        ```

## Assignment 1 with VPL

    - Run Deepak's script on dataset to create tables
    - Create test dataset
        + Load it on all servers

    - What is the "correct" script format?

    - Answers of SQL queries?
        + Are the queries correct?
        + Ambiguities?

    - What if psql throws an error?

    - Grade in background but don't show

    - Problems
        - We want to give `CREATE VIEW` permission
        - Name clashes of views in single Database
        - Resource usage of old views

    - Solution
        - Create new database for every evaluation?
            - `WITH TEMPLATE`
            - Resource usage, Timing? - Depends on test dataset

    - TODO: Check if sql files can contain `\` commands

    - Setup DB on VPL 2/3

```bash
ip addr show dev ens3 | grep "inet " | perl -ne '/inet (.*)\// && print $1'
```
