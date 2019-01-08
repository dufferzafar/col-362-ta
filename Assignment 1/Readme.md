
# Assignment 1


## Server Work

* Passwordless
* Upgrade

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

* Install Postgres
    - Latest, v11.0
        + Not in repos: tarball, add-apt-repo 
    - Load HW 1 Data
    - Test working
        + Run SQL queries etc.
    - psqli

* VPL + Postgres
    - Frontend / Activity
        + SQL
        + HW1 SQL

    - Backend / VPL
        + evaluate.sh
            * bash script
            * run .sql via psql

* Assignment 1 VPL
