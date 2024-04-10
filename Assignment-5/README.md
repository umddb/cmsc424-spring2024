# Assignment 4: Apache Spark

The goal of this assignment is to learn how to do large-scale data analysis tasks using Apache Spark: for this assignment, we will use relatively small datasets and  we won't run anything in distributed mode; however Spark can be easily used to run the same programs on much larger datasets.

### Getting Started with Spark

This guide is basically a summary of the excellent tutorials that can be found at the [Spark website](http://spark.apache.org).

[Apache Spark](https://spark.apache.org) is a relatively new cluster computing framework, developed originally at UC Berkeley. It significantly generalizes the 2-stage Map-Reduce paradigm (originally proposed by Google and popularized by open-source Hadoop system); Spark is instead based on the abstraction of **resilient distributed datasets (RDDs)**. An RDD is basically a distributed collection of items, that can be created in a variety of ways. Spark provides a set of operations to transform one or more RDDs into an output RDD, and analysis tasks are written as chains of these operations.

Spark can be used with the Hadoop ecosystem, including the HDFS file system and the YARN resource manager. 

### Installing Spark

The Docker image already includes the spark distribution. But if you want to set it up manually: 

1. Download the Spark package at http://spark.apache.org/downloads.html. We will use **Version 3.5.0, Pre-built for Hadoop 3.3 or later**.
2. Move the downloaded file to the `Assignment-5/` directory (so it is available in '/data/Assignment-5'), and uncompress it using: 
`tar zxvf spark-3.5.0-bin-hadoop3.tgz`
3. This will create a new directory: `spark-3.5.0-bin-hadoop3/`. 
4. Set the SPARKHOME variable: `export SPARKHOME=/data/Assignment-3/spark-3.5.0-bin-hadoop3/` (modify appropriately if it is downloaded somewhere else).
5. Note: in the image we have provided, SPARKHOME is `/spark` -- you can always move the downloaded stuff there, but it won't persist when you quit the docker image. 

We are ready to use Spark. 

### Spark and Python

Spark primarily supports three languages: Scala (Spark is written in Scala), Java, and Python. We will use Python here -- you can follow the instructions at the tutorial and quick start (http://spark.apache.org/docs/latest/quick-start.html) for other languages. The Java equivalent code can be very verbose and hard to follow. The below shows a way to use the Python interface through the standard Python shell.

### Jupyter Notebook

To use Spark within the Jupyter Notebook (and to play with the Notebook we have provided), you can do:
	```
	PYSPARK_PYTHON=/usr/bin/python3 PYSPARK_DRIVER_PYTHON="jupyter" PYSPARK_DRIVER_PYTHON_OPTS="notebook --allow-root --no-browser --ip=0.0.0.0 --port=8881" $SPARKHOME/bin/pyspark
	```
You need to make sure you are mapping the port 8881 for this to work.

### PySpark Shell

You can also use the PySpark Shell directly.

1. `$SPARKHOME/bin/pyspark`: This will start a Python shell (it will also output a bunch of stuff about what Spark is doing). The relevant variables are initialized in this python
shell, but otherwise it is just a standard Python shell.

2. `>>> textFile = sc.textFile("README.md")`: This creates a new RDD, called `textFile`, by reading data from a local file. The `sc.textFile` commands create an RDD
containing one entry per line in the file.

3. You can see some information about the RDD by doing `textFile.count()` or `textFile.first()`, or `textFile.take(5)` (which prints an array containing 5 items from the RDD).

4. We recommend you follow the rest of the commands in the quick start guide (http://spark.apache.org/docs/latest/quick-start.html). Here we will simply do the Word Count application.

#### Word Count Application

The following command (in the pyspark shell) does a word count, i.e., it counts the number of times each word appears in the file `README.md`. Use `counts.take(5)` to see the output.

`>>> counts = textFile.flatMap(lambda line: line.split(" ")).map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)`

Here is the same code without the use of `lambda` functions.

```
def split(line): 
    return line.split(" ")
def generateone(word): 
    return (word, 1)
def sum(a, b):
    return a + b

textfile.flatMap(split).map(generateone).reduceByKey(sum)
```

The `flatmap` splits each line into words, and the following `map` and `reduce` do the counting (we will discuss this in the class, but here is an excellent and detailed
description: [Hadoop Map-Reduce Tutorial](http://hadoop.apache.org/docs/r1.2.1/mapred_tutorial.html#Source+Code) (look for Walk-Through).

The `lambda` representation is more compact and preferable, especially for small functions, but for large functions, it is better to separate out the definitions.

### Running it as an Application

Instead of using a shell, you can also write your code as a python file, and *submit* that to the spark cluster. The `project5` directory contains a python file `wordcount.py`, which runs the program in a local mode. To run the program, do: `$SPARKHOME/bin/spark-submit wordcount.py`

### More...

We encourage you to look at the [Spark Programming Guide](https://spark.apache.org/docs/latest/programming-guide.html) and play with the other RDD manipulation commands. You should also try out the Scala and Java interfaces.

### Assignment Details

We have provided a Python file: `spark_assignment.py`, that initializes the folllowing RDDs:
* An RDD consisting of tuples from Stackexchange "Users" table (`se_users.json`), each tuple as a dictionary
* An RDD consisting of tuples from Stackexchange "Posts" table (`se_posts.json`), each tuple as a dictionary
* An RDD consisting of lines from a Shakespeare play (`play.txt`)
* An RDD consisting of lines from a log file (`NASA_logs_sample.txt`)
* An RDD consisting of JSON documents pertaining to all the Noble Laureates over last few years (`prize.json`)
* Two RDDs consisting of "movies" and "ratings" from the MovieLens Dataset (https://grouplens.org/datasets/movielens/)

The file also contains some examples of operations on these RDDs. Before beginning any of the tasks, you should inspect the RDDs (e.g., using `print(rdd.take(10))`).

Your tasks are to fill out the 16 functions that are defined in the `functions.py` file (starting with `task`). The amount of code that you write would typically be small (several would be one-liners), but some of the tasks do require more code.

**Task 1 (0.25)**: Use `filter` to find all posts where 'OwnerUserId' and 'viewcount' are not `null` (None in python) and viewCount is atleast 10000, and then a `map` so that the output RDD has tuples of the form: (ID, Title, OwnerUserId, ViewCount). Note that postsRDD contains dictionaries -- see the contents by running `postsRDD.take(10)` -- our desired output is tuples.

- **Task 2 (0.25)**: Use `flatMap` on the moviesRDD to create an RDD (ID, Genre), listing each of the genres for each movie as a separate tuple. If a movie has no genres, it should not appear in the output RDD.

- **Task 3 (0.25)**: The goal is to find the number of movies per year for each of the genres using `moviesRDD`. So the outputRDD should be of the form: (genre, year, num-movies). Use `map` to extract the year from the title (using a regular expression), `flatmap` similar to above, and then an appropriate `reduceByKey`. Ignore any movies where there is no year information in the title.

Note: Treat '(no genres listed)' as a genre (it appears for some movies). One of the outputs like that looks like: _('(no genres listed)', '1957', 1)_

- **Task 4 (0.25)**: The goal here is to find the 2 lexicographically smallest genres for each user across all the movies that they rated. So the outputRDD should be contain tuples of the form: ('1', ['Adventure', 'Fantasy']), assuming those two genres are the lexicographically smallest across all the genres associated with the movies the user '1' has rated. You will first have to `join` the two RDDs to connect users with movies they have rated, and then a `reduceByKey` with an appropriate function to find the two lexicographically smallest genres across all the movies they have rated. Note that, in `ratingsRDD`, the userID is first and movieID is second element. 

- **Task 5 (0.25)**: Using the moviesRDD, create an RDD where the key is a 2-tuple (title-word, genre), where the former is a word in the title, and the latter is a genre associated with the movie.  The value associated with the key should be the number of movies in which the title-word is in the title, and the genre is in the list of genres for that movie. This will require a couple of `flatMap`s and an `aggregateByKey` to count. 

Note: When splitting the title into words, first remove the following special characters: `,`, `(`, `)`, `:`, and then split using `.split()`. So in the output, you should have tuples like the following:
_(('!', 'Comedy'), 2)_ (where `!` ends up getting treated as a word).

- **Task 6 (0.25)**: Let's compute the number of times each user has used a specific tag using `postsRDD`. First filter out all posts where owneruserid is null, use `flatMap` to split up the tags, and then a reduceByKey can be used to compute the number of times each (user, tag) pair appears. You may need a `map` before applying `reduceByKey`. 

_Answer for User 7: [((7, 'mysql'), 2), ((7, 'my.cnf'), 1), ((7, 'version-control'), 1), ((7, 'schema'), 1)]_

- **Task 7 (0.25)**: Complete the function that takes as input the `ratingsRDD` and computes the average
rating for each user across all the movies they rated.  The output should be an RDD of 2-tuples of the form
`('1', 2.87)` (not the correct answer).  You can either use `aggregateByKey` or a `reduceByKey` followed by a
`map`. 

Note: Do not round the output. First few tuples look like: 
_('1', 4.366379310344827), ('10', 3.2785714285714285), ('100', 3.945945945945946), ('101', 3.557377049180328)_

- **Task 8 (0.25)**: Complete the function that takes as input the `ratingsRDD` and computes the `mode` rating for each movie across all users (i.e., the rating that was most common for that movie). If there are ties, pick the higher rating. Easiest way to do this would be a `groupByKey` followed by a map to compute the `mode`. Note: unlike the previous question, here we are aggregating over movies, not users.

Note: Do not convert the ratings to a float. Note that the ratings go from '0.5' to '5.0', in increments of 0.5.
Few of the output tuples: _('1', '4.0'), ('10', '3.0'), ('100', '3.0'), ('100044', '4.0'), ('100068', '3.5')_


- **Task 9 (0.25)**: For `logsRDD`, write a function that computes the number of log requests for each day of the year. So the output should be an RDD with records of the form `(1, 100)` (not the correct answer). This can be done through a `map` to extract the day (the provided sample file only has 2 days), followed by a group by aggregate.

_Answer on provided sample file: [(1, 5000), (2, 5000)]_

- **Task 10 (0.25)**: Write just the flatmap function `task10_flatmap` that operates on `playRDD` -- for each line, it should execute a few of the common "sanitization" steps that are often done on text data before further processing (e.g., before tokenization for ML). Specifically: (1) make everything lowercase, (2) expand a specific list of words like "don't" with "do not", (3) replace all non-alphanumerical characters with " ", and (4) remove all stop (very common) words. 
For (2), do: "is't" --> "is it", "'twere" --> "it were", and "'tis" --> "it is"
For (4), remove: "is", "the", "in", "s".
The function should return a list of words after all these steps in order.

_Answer on the first three lines: ['act', 'i', 'scene', 'i', 'before', 'leonato', 'house', 'enter', 'leonato', 'hero', 'and', 'beatrice', 'with', 'a', 'messenger']_

- **Task 11 (0.25)**: Let's look for users with potentially anomalous behavior. Specifically, we want to find all users with > 50 posts, but with average score per post < 10. Use the `postsRDD` for this purpose, with an appropriate `map`, `reduceByKey`, and `filter`. Output the userid as well as the post count and the average score.

_A few answers: [(154, 197, 3.979695431472081), (630, 211, 9.341232227488153), (26626, 64, 2.734375)]_

- **Task 12 (0.25)**: Write a sequence of transformations starting from `prizeRDD` that returns an PairRDD where the key is the `category` (`physics` etc), and the value is a list of all Nobel Laureates for that category (just their surnames). Make sure the final values are `list`s, and not some other class objects (if you do a `take(5)`, it should print out the lists).

- **Task 13 (0.25)**: This function operates on the `logsRDD`. It takes as input a list of *dates* and returns an RDD with "hosts" that were present in the log on all of those dates. The dates would be provided as strings, in the same format that they appear in the logs (e.g., '01/Jul/1995' and '02/Jul/1995').  The format of the log entries should be self-explanatory, but here are more details if you need: [NASA Logs](http://ita.ee.lbl.gov/html/contrib/NASA-HTTP.html) Try to minimize the number of RDDs you end up creating. Note that the list of dates may contain more than 2 entries.

- **Task 14 (0.25)**: On the `logsRDD`, for two given days (provided as input analogous to Task 9 above), use a 'cogroup' to create the following RDD: the key of the RDD will be a host, and the value will be a 2-tuple, where the first element is a list of all URLs fetched from that host on the first day, and the second element is the list of all URLs fetched from that host on the second day. Use `filter` to first create two RDDs from the input `logsRDD`.


- **Task 15 (0.25)**: Here we will try to do something similar to "nearest neighbors" that we did in an earlier assignment for recommendations. For each user, we would like to find the closest neighbor by Jaccard coefficient by looking at the movies they rated (we will ignore the actual ratings -- in reality, we would likely want incorporate that in the distance measure). Since we need to compare each user with every other user, this would require a Cartesian product -- given the number of users, this should be doable but let's restrict to first 100 users (i.e., userid <= 100). 
Specifically: for each user u1 (with id <= 100), we need to find the user u2 (with id <= 100) who has the highest Jaccard coefficient by comparing the sets of movies they watched. We have provided the function to do Jaccard computation, and as well as an initial transformation on the ratingsRDD to collect all the rated movies by user for first 100 users. 

_Example answer: ('4', ('57', 0.1270358306188925))_

- **Task 16 (0.25)**: [Bigrams](http://en.wikipedia.org/wiki/Bigram) are sequences of two consecutive words. For example, the previous sentence contains the following bigrams: "Bigrams are", "are simply", "simply sequences", "sequences of", etc. Your task is to write a bigram counting application for counting the bigrams in the `motivation`s of the Nobel Prizes (i.e., the reason they were given the Nobel Prize). The return value should be a PairRDD where the key is a bigram, and the value is its count, i.e., in how many different `motivations` did it appear. Don't assume 'motivation' is always present.


### Sample results.txt File
You can use `spark-submit` to run the `spark_assignment.py` file, but it would be easier to develop with `pyspark` (by copying the commands over). 
