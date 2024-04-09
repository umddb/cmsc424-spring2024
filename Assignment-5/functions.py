import json
import re

# A hack to avoid having to pass 'sc' around
dummyrdd = None
def setDefaultAnswer(rdd): 
    global dummyrdd
    dummyrdd = rdd

def task1(postsRDD):
    return dummyrdd

def task2(moviesRDD):
    return dummyrdd

def task3(moviesRDD):
    return dummyrdd

def task4(moviesRDD, ratingsRDD):
    return dummyrdd

def task5(moviesRDD):
    return dummyrdd

def task6(postsRDD):
    return dummyrdd

def task7(ratingsRDD):
    return dummyrdd

def task8(ratingsRDD):
    return dummyrdd

def task9(logsRDD):
    return dummyrdd

def task10_flatmap(line):
    return line

def task11(postsRDD):
    return dummyrdd

def task12(nobelRDD):
    return dummyrdd

def task13(logsRDD, l):
    return dummyrdd

def task14(logsRDD, day1, day2):
    return dummyrdd

def task15(ratingsRDD):
    def jaccard(set_a, set_b):
        # Calculate the intersection of sets
        intersection = len(set_a.intersection(set_b))

        # Calculate the union of sets
        union = len(set_a.union(set_b))

        # Compute the Jaccard coefficient
        jaccard = intersection / union if union != 0 else 0
        return jaccard

    t15_1 = ratingsRDD \
            .filter(lambda t: int(t[0]) <= 100) \
            .map(lambda t: (t[0], t[1])) \
            .groupByKey() \
            .map(lambda l: (l[0], list(l[1])))

    t15 = t15_1

    return t15

def task16(nobelRDD):
    return dummyrdd
