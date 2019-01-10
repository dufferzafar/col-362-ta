
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

    * Setting up roles and database

        ```sql
        CREATE ROLE vpl_user LOGIN;
        CREATE DATABASE vpl_db OWNER postgres;
        ```

## Assignment 1 with VPL

    - Run Deepak's script on dataset to create tables
    - Create test dataset
        + Load it on both servers

    - What is the "correct" script format?
    - Answers of SQL queries?
        + Are the queries correct?
        + Ambiguities?

    - How will grading happen?

    - What if psql throws an error?

    - Grade in background but don't show


```bash
ip addr show dev ens3 | grep "inet " | perl -ne '/inet (.*)\// && print $1'
```
