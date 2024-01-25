## Assignment 1: SQL Assignment, CMSC424, Spring 2024 (Part 1)

*The assignment is to be done by yourself.*

*Keep in mind that this assignment has a Part 2 which is available on GradeScope.*

The following assumes you have gone through PostgreSQL instructions and have ran some queries on the `university` database. 
It also assumes you have cloned the git repository, and have done a `git pull` to download the directory `Assignment-1`. The files are:

1. README.md: This file
1. populate-se.sql: The SQL script for creating the data.
1. queries.py: The file where to enter your answer (and to be uploaded to gradescope)
1. SQLTesting.py: File to be used for running the queries (in `queries.py`) against the database

### Getting started
If you are using the provided docker image, the database should already be loaded. If not (or if you are using another instance of PostgreSQL), you can follow these instructions.

1. Create a new database using: 'createdb stackexchange'
1. Load the data using: 'psql -f populate-se.sql' (or you can do \i populate-se.sql from within psql)
1. There will be a lot of errors -- ignore those -- we are using a subset of the posts and users, and we are letting PostgreSQL reject inserts that violate referential integrity.

### Schema 
The dataset contains a subset of the data from the DBA Stack Exchange website (https://dba.stackexchange.com). The main tables are:
- Users: containing basic information about the  users of the platform
- Posts: both questions and answers are considered posts -- a post of type "answer" has a reference to the parent post with the question.
- Comments, Votes: contain information about the comments and votes on posts
- Badges: list out the badges that a user has received. 

You can see the a detailed discussion of the different fields at https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede/2678#2678.  Note that we are only using a subset of the fields as can be seen in the `populate-se.sql` file.

In many cases (especially for complex queries or queries involving `max` or `min`), you will find it easier to create temporary tables using the `with` construct. This also allows you to break down the full query and makes it easier to debug.

You don't have to use the "hints" if you don't want to; there might be simpler ways to solve the questions.

### Testing and submitting using SQLTesting.py
Your answers (i.e., SQL queries) should be added to the `queries.py` file. A simple query is provided for the first answer to show you how it works.
You are also provided with a Python file `SQLTesting.py` for testing your answers.

- We recommend that you use `psql` to design your queries, and then paste the queries to the `queries.py` file, and confirm it works.

- SQLTesting takes quite a few options: use `python3 SQLTesting.py -h` to see the options.

- To get started with SQLTesting, do: `python3 SQLTesting.py -i` -- that will run each of the queries and show you your answer.

- If you want to run your query for Question 1, use: `python3 SQLTesting.py -q 1`. 

- `-i` flag to SQLTesting will run all the queries, one at a time (waiting for you to press Enter after each query).

- **Note**: We will essentially run a modified version of `SQLTesting.py` that compares the returned answers against correct answers. So it imperative that `python3 SQLTesting.py` runs without errors.

### Submission Instructions
Submit the `queries.py` file on Gradescope under Assignment 1. 
      
### Assignment Questions
See `queries.py` file.
