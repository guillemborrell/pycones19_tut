Persistency
===========

Let's talk about saving data somewhere.

We'll start with a SQL database, which is kind of the hardest thing to do efficiently in Python

PostgreSQL
----------

Assuming Debian buster, and PostgreSQL 11, we'll check that the service is OK with

.. code::

    $> sudo systemctl status postgresql
    ● postgresql.service - PostgreSQL RDBMS
       Loaded: loaded (/lib/systemd/system/postgresql.service; enabled; vendor preset: enabled)
       Active: active (exited) since Sun 2019-08-25 12:03:08 UTC; 9h ago
      Process: 604 ExecStart=/bin/true (code=exited, status=0/SUCCESS)
     Main PID: 604 (code=exited, status=0/SUCCESS)
    Aug 25 12:03:08 flappybird systemd[1]: Starting PostgreSQL RDBMS...
    Aug 25 12:03:08 flappybird systemd[1]: Started PostgreSQL RDBMS.

Then we will create a user and a database as follows

.. code::

    $> sudo -u postgres psql
    psql (11.5 (Debian 11.5-1+deb10u1))
    Type "help" for help.
    postgres=# create database flappystream;
    CREATE DATABASE
    postgres=# create user flappystream with encrypted password 'flappystream';
    CREATE ROLE
    postgres=# grant all privileges on database flappystream to flappystream;
    GRANT

The user can also be created using the ``createuser`` command that is installed with the database. You can log into the
database, again within the same server, with

.. code::
    psql -h localhost -U flappystream -W flappystream
    flappystream=> \dt
              List of relations
     Schema | Name | Type  |    Owner
    --------+------+-------+--------------
     public | logs | table | flappystream
    (1 row)

You must specify the host, otherwise it will try to access the database using a UNIX socket.