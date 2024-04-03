from pyspark import SparkContext
from functions import *
import re
import json
import csv
from io import StringIO
import json
import sys

sc = SparkContext("local", "Simple App")
setDefaultAnswer(sc.parallelize([0]))

## Load data into RDDs
usersRDD = sc.textFile("datafiles/se_users.json").map(json.loads)
postsRDD = sc.textFile("datafiles/se_posts.json").map(json.loads)
playRDD = sc.textFile("datafiles/play.txt")
logsRDD = sc.textFile("datafiles/NASA_logs_sample.txt")
nobelRDD = sc.textFile("datafiles/prize.json").map(json.loads)

# Movielens Ratings
# The complicated setup is needed to properly parse the CSV file, and also to skip the header row using sparkContext
def parse_csv(line):
    reader = csv.reader(StringIO(line))
    return next(reader)

# Let's make RDDs for the Movie Lens Files 
csvData1 = sc.textFile("datafiles/ml-latest-small/movies.csv")
moviesRDD = csvData1.zipWithIndex().filter(lambda line: line[1] != 0).map(lambda line: line[0]).map(parse_csv)

# For ratings, we will skip the timestamp for simplicity
csvData2 = sc.textFile("datafiles/ml-latest-small/ratings.csv")
ratingsRDD = csvData2.zipWithIndex().filter(lambda line: line[1] != 0).map(lambda line: line[0].split(",")[0:3])
        
        
if len(sys.argv) < 2:
   task_to_run = None
else:
   task_to_run = int(sys.argv[1])

## Each of the tasks requires you to write one function
## The code below iterates through the tasks
tasks = [
    (1, task1, postsRDD),
    (2, task2, moviesRDD),
    (3, task3, moviesRDD),
    (4, task4, (moviesRDD, ratingsRDD)), # two inputs
    (5, task5, moviesRDD),
    (6, task6, postsRDD),
    (7, task7, ratingsRDD),
    (8, task8, ratingsRDD),
    (9, task9, logsRDD),
    (10, task10_flatmap, playRDD), # different format
    (11, task11, postsRDD),
    (12, task12, nobelRDD),
    (13, task13, logsRDD), # different format
    (14, task14, logsRDD),
    (15, task15, ratingsRDD),
    (16, task16, nobelRDD),
]

for task in tasks:
     ## tasks where you have to write a function that takes in an RDD as input
     if task_to_run is None or task_to_run == task[0]:
         print("=========================== Task {}".format(task[0]))
         if task[0] in [1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 15, 16]:
            r = task[1](task[2])
            for x in r.takeOrdered(5):
                print(x)

         ## tasks where you have to write a function that takes in two RDDs as input
         elif task[0] in [4]:
            r = task[1](task[2][0], task[2][1])
            for x in r.takeOrdered(5):
                print(x)

         ## tasks where you have to write a flatMap function
         elif task[0] in [10]:
            r = task[2].flatMap(task[1]).distinct()
            print(r.takeOrdered(5))

         ## special cases
         elif task[0] in [13]:
            r = task[1](task[2], ['01/Jul/1995', '02/Jul/1995'])
            for x in r.takeOrdered(5):
                print(x)
         elif task[0] in [14]:
            r = task[1](task[2], '01/Jul/1995', '02/Jul/1995')
            for x in r.takeOrdered(5):
                print(x)


## print out the expected answer
if task_to_run is not None:
    with open('results.txt', 'r') as f:
        start_printing = False
        for line in f:
            if "========= Task {}\n".format(task_to_run) in line:
               start_printing = True
            if "========= Task {}\n".format(task_to_run+1) in line:
               start_printing = False
            
            if start_printing:
                print(line.strip())
