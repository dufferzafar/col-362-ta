
# Project 1

## Components

**datadrop/**

A flask application to allow uploading of data dumps.

Built with Dropzone etc.

**logview/**

A flask appliaction to view PostgreSQL logs as an HTML table.

**massmail/**

A script to send email from IIT D account to lots of students.

## Todo?

* Setup
    - VMs: Create role for each group

* Deploy
    - Multiple machines
        + Flask app on each VM
        + logview on each VM
        + Ports?

        + haproxy

* Add a function to process the dump
    - Get a test dump? Get pgdump from Ass1 DB
    - `def pg_load(user, path)`
    - Run proper `pg_restore`
    - Return output / error

* `datadrop`
    - Redesign the Dropzone
        + Take ideas from [this page](https://www.dropzonejs.com/bootstrap.html).
        + Make errors show up in a `div` below the zone

* `logview`
    - Run instances on each machine
    - Give ma'am the address of vpl1's logview
    - Which redirects to the one that the group would use (group_num % 3)
    - Currently, it can only display the log of the host it runs on
    - But since students will connect to different hosts, how will it display log from them?

* Code refactor

* Someone can try to bruteforce the HTTP basic auth of other users
    - Increase the password length to be 9 numbers: 3-3-3
    - [Rate limit via Flask?](https://flask-limiter.readthedocs.io/en/stable/)

* Full Demo (by Thursday 4 PM)
    - Setup
        - Create schema of a DB
        - Load a dataset into the DB
        - Dump the DB

    - datadrop
        - login as group_0
        - Test upload
            + Also test 500MB, 1GB, 2GB dumps!

    - logview
        - Run a script that queries data from DB
        - Ensure all queries are displayed

* Float a group sheet (after Thursday meeting)
    - Ask email IDs of all groups
    - Estimated data size? (not compressed)
    - Assign group numbers so that distribution is even
