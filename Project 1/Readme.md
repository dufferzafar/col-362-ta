
# Project 1

## Data Dump

- What format
    + `pgdump` has a bunch of them

    + Does it work on windows as well?
        * If not, Ostrich!

## Data Submission

### Upload dump to cloud service

- Students submit a `data.sh` to a Moodle activity
    * Which has the link of the their file
    * Runs and downloads the dump

- Data loading - Semi automated
    + Download all `group_$num_data.sh`
    + Run them
    + Fix their dump files
        * Change database names to `group_$num`
    + Load them to different machines: `vpl1,2,3`
        * `group_$num % 3`
        * `pg_restore`

    + If multiple students upload: Penalty of 1 marks!

- Issues

    + Hard to enforce deadlines
        * as files can be updated later
        * and we'll have to manually check their timestamps.

### Custom Upload Application

- Write a webapp in Python/Flask

    + Users upload their dump files

    + A script runs that tries to load the dump via `pg_restore`
    + If an error occurs, it is displayed on the page itself

    + Implementation Details
        * [Handle large file uploads](https://stackoverflow.com/questions/44727052/handling-large-file-uploads-with-flask)

        * [Run multiple instances & use a loadbalancer](https://github.com/cliftonlabs/mini-load-balancer/blob/master/python-flask/haproxy.cfg)

- Issues

    + All dumps will be loaded by `vpl_user` 

    + How will users be linked to group numbers?
        * Create separate DB users

        * OAUTH Kerberos ID?


## Caveats

- How will we ensure that students are connecting to our database and not their own?

- Do we need to have separate DB users & databases per group?
    + Prevents them from messing with each anothers' data
        * Is this really required?

    + Not hard to do if we're loading the data manually

## Deliverables

* Setup phase
    - Create roles for each group
    - Setup their privileges?

* Mass mailer

* Load App
    - Python/Flask/Dropzone
    - Login: [Basic Auth](https://flask-basicauth.readthedocs.io/en/latest/#flask.ext.basicauth.BasicAuth.check_credentials) or Form post?
    
    - `def pg_load()`

    - HAProxy

* Log App
    - Jinja template
    - with Bootstrap table
        + SQL Syntax highlight?
