import psycopg2
import os
import sys
import datetime
from collections import Counter
from types import *
import argparse

from queries import *

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--interactive', help="Run queries one at a time, and wait for user to proceed", required=False, action="store_true")
parser.add_argument('-q', '--query', type = int, help="Only run the given query number", required=False)
args = parser.parse_args()

interactive = args.interactive

conn = psycopg2.connect("host=127.0.0.1 dbname=stackexchange user=root password=root")
cur = conn.cursor()

print("Dropping and creating commentscopy, lengthfiltertype")
cur.execute("drop table if exists commentscopy;")
cur.execute("drop type if exists lengthfiltertype;")
cur.execute("create table commentscopy as (select * from comments);")
cur.execute("CREATE TYPE lengthfiltertype AS ENUM ('Long', 'Medium', 'Short')")
conn.commit()

print("Dropping and creating trigger UpdateStarUsers on badges")
cur.execute("drop trigger if exists UpdateStarUsers on badges;")
conn.commit()

print("Dropping and creating tables/views postssummary, starusers, answered")
cur.execute("drop table if exists starusers;")
cur.execute("create table starusers as select u.ID, count(b.ID) as NumBadges from users u left join badges b on u.id = b.userid group by u.id having count(b.ID) > 10;")


cur.execute("drop view if exists postssummary;")
cur.execute("drop table if exists answered;")
cur.execute("create table answered as select p1.owneruserid as parent, p2.owneruserid as child from posts p1, posts p2 where p1.id = p2.parentid and p1.owneruserid != p2.owneruserid;")
conn.commit()

input('Press enter to proceed')


test_queries_to_run = [None] * 100
test_queries_to_run[1] = ("SELECT * FROM commentscopy where id < 10 order by id", 
                                "-- Result (should have appropriate new columns)") 
test_queries_to_run[2] = ("SELECT * FROM commentscopy where id < 10 order by id", 
                                "-- Result (should have appropriate new columns with appropriate values)") 
test_queries_to_run[3] = ("select * from commentscopy where id in (6081, 6251); ",
                                "-- Result should not have any tuples")
test_queries_to_run[4] = ("select * from commentscopy where id between 50000 and 50010", 
                                "-- Result should contain the new 10 tuples along with older tuples with those ids")
test_queries_to_run[5] = ("select * from information_schema.table_constraints tc where tc.table_name = 'commentscopy';", 
       "-- Result (should have the 5 new constraints for commentscopy, but not all the information")

test_queries_to_run[7] = ("select * from PostsSummary where id < 10", 
                                "-- Result (should have 8 rows with appropriate counts)")
test_queries_to_run[9] = ("select id, title, numvotes(id) from posts limit 20", 
                                "-- Result")
test_queries_to_run[10] = ("select userposts(7)", "-- Result")
test_queries_to_run[11] = ( 'SELECT n.nspname as "Schema", p.proname as "Name", pg_catalog.pg_get_function_result(p.oid) as "Result data type" FROM pg_catalog.pg_proc p LEFT JOIN pg_catalog.pg_namespace n ON n.oid = p.pronamespace WHERE p.proname = \'updatestarusers\'' ,
                "-- Result (should list the trigger function)")

for i in range(0, 15):
    # If a query is specified by -q option, only do that one
    if args.query is None or args.query == i:
        try:
            if interactive:
                os.system('clear')
            print("========== Executing Query {}".format(i))
            print(queries[i])
            cur.execute(queries[i])

            if i in [6, 8, 13, 14]:
                ans = cur.fetchall()

                print("--------- Your Query Answer ---------")
                for t in ans:
                    print(t)
                print("")
            elif i in [1, 2, 3, 4, 5, 7, 9, 10, 11]:
                conn.commit()
                print("--------- Running {} -------".format(test_queries_to_run[i][0]))
                cur.execute(test_queries_to_run[i][0])
                ans = cur.fetchall()
                print(test_queries_to_run[i][1])
                for t in ans:
                    print(t)
                print("")
            elif i in [12]:
                conn.commit()
                print("************* Testing Insert -----------")
                query_string = "insert into badges values(500001, 655 , 'Famous Question', to_date('2024-02-20', 'YYYY-MM-DD'), 3)"
                cur.execute(query_string)
                conn.commit()
                query_string = "select * from starusers where id = 655"
                print("--------- Running {} -------".format(query_string))
                cur.execute(query_string)
                ans = cur.fetchall()
                print("-- Result (should list 655 with 11 badges)")
                for t in ans:
                    print(t)
                print("")

                print("************* Testing Delete -----------")
                query_string = "delete from badges where id = 500001"
                cur.execute(query_string)
                conn.commit()
                query_string = "select * from starusers where id = 655"
                print("--------- Running {} -------".format(query_string))
                cur.execute(query_string)
                ans = cur.fetchall()
                print("-- Result (should not list 655)")
                for t in ans:
                    print(t)
                print("")

                print("************* Testing Update -----------")
                query_string = "select * from starusers where id = 6025 or id = 15684"
                print("--------- Running {} before update -------".format(query_string))
                cur.execute(query_string)
                ans = cur.fetchall()
                print("-- Result (should list 15684 with 11 badges, but no 6025)")
                for t in ans:
                    print(t)
                print("")

                query_string = "update badges set userid = 6025 where id = 27880"
                cur.execute(query_string)
                conn.commit()
                query_string = "select * from starusers where id = 6025 or id = 15684"
                print("--------- Running {} after update -------".format(query_string))
                cur.execute(query_string)
                ans = cur.fetchall()
                print("-- Result (should list 6025 with 11 badges, but no 15684)")
                for t in ans:
                    print(t)
                print("")
                
            if interactive:
                input('Press enter to proceed')
                os.system('clear')
        except:
            print(sys.exc_info())
            raise
