import psycopg2
import os
import sys
import datetime
from collections import Counter
from types import *
import argparse
import pymongo
import pprint

from queries import *

client = pymongo.MongoClient("localhost", 27017)
db = client["analytics"]

for idx, q in enumerate([query0, query1, query2, query3, query4, query5, query6, query7, query8, query9, query10, query11, query12, query13, query14, query15, query16, query17]):
    print("============ Executing Query {}".format(idx))
    results = list(q(db))

    for r in results[:10]:
        pprint.pprint(r)
