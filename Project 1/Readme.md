
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

* Redesign the Dropzone
    - Take ideas from [this page](https://www.dropzonejs.com/bootstrap.html).
    - Make errors show up in a `div` below the zone

* Add a function to process the dump
    - `def pg_load(user, path)`
    - Run proper `pg_restore`
    - Return output / error

* Someone can try to bruteforce the HTTP basic auth of other users
    - [Rate limit via Flask?](https://flask-limiter.readthedocs.io/en/stable/)

* `logview`
    - Currently, it can only display the log of the host it runs on
    - But since students will connect to different hosts, how will it display log from them?
