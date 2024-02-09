queries = ["" for i in range(0, 17)]

### 0. List all the users who have at least 1000 UpVotes.
### Output columns and order: Id, Reputation, CreationDate, DisplayName
### Order by Id ascending
queries[0] = """
select Id, Reputation, CreationDate,  DisplayName
from users
where UpVotes >= 1000
order by Id asc;
"""

### 1. Write a query to find all Posts who satisfy one of the following conditions:
###        - the post title contains 'postgres' and the number of views is at least 50000
###        - the post title contains 'mongodb' and the number of views is at least 25000
### The match should be case insensitive
###
### Output columns: Id, Title, ViewCount
### Order by: Id ascending
queries[1] = """
select 0;
"""

### 2. Count the number of the Badges for the user with DisplayName 'JHFB'.
###
### Output columns: Num_Badges
queries[2] = """
select 0;
"""

### 3. Find the Users who have received a "Guru" badge, but not a "Curious" badge.
### Only report a user once even if they have received multiple badges with the above names.
###
### Hint: Use Except (set operation).
###
### Output columns: UserId
### Order by: UserId ascending
queries[3] = """
select 0;
"""

### 4. "Tags" field in Posts lists out the tags associated with the post in the format "<tag1><tag2>..<tagn>".
### Find the Posts with at least 4 tags, with one of the tags being sql-server-2008 (exact match).
### Hint: use "string_to_array" and "cardinality" functions.
### Output columns: Id, Title, Tags
### Order by Id
queries[4] = """
select 0;
"""

### 5. SQL "with" clause can be used to simplify queries. It essentially allows
### specifying temporary tables to be used during the rest of the query. See Section
### 3.8.6 (6th Edition) for some examples.
###
### Write a query to find the name(s) of the user(s) with the largest number of badges. 
### We have provided a part of the query to build a temporary table.
###
### Output columns: Id, DisplayName, Num_Badges
### Order by Id ascending (there may be more than one answer)
queries[5] = """
with temp as (
        select Users.Id, DisplayName, count(*) as num_badges 
        from users join badges on (users.id = badges.userid)
        group by users.id, users.displayname)
select *
from temp;
"""

### 6. "With" clauses can be chained together to simplify complex queries. 
###
### Write a query to associate with each user the number of posts they own as well as the
### number of badges they have received, assuming they have at least one post and
### one badge. We have provided a part of the query to build two temporary tables.
###
### Restrict the output to users with id less than 100.
###
### Output columns: Id, DisplayName, Num_Posts, Num_Badges
### Order by Id ascending
queries[6] = """
with temp1 as (
        select owneruserid, count(*) as num_posts
        from posts
        group by owneruserid),
temp2 as (
        select userid, count(*) as num_badges
        from badges
        group by userid)
select * 
from temp1;
"""

### 7. A problem with the above query is that it may not include users who have no posts or no badges.
### Use "left outer join" to include all users in the output.
###
### Feel free to modify the "with" clauses to simplify the query if you like.
###
### Output columns: Id, DisplayName, Num_Posts, Num_Badges
### Order by Id ascending
queries[7] = """
with temp1 as (
        select owneruserid, count(*) as num_posts
        from posts
        group by owneruserid),
temp2 as (
        select userid, count(*) as num_badges
        from badges
        group by userid)
select *
from temp1;
"""

### 8. List the users who have made a post in 2009.
### Hint: Use "in".
###
### Output Columns: Id, DisplayName
### Order by Id ascending
queries[8] = """
select 0;
"""

### 9. Find the users who have made a post in 2009 (between 1/1/2009 and 12/31/2009)
### and have received a badge in 2011 (between 1/1/2011 and 12/31/2011).
### Hint: Use "intersect" and "in".
###
### Output Columns: Id, DisplayName
### Order by Id ascending
queries[9] = """
select 0;
"""

### 10. Write a query to output a list of posts with comments, such that PostType = 'Moderator nomination' 
### and the comment has score of at least 10. So there may be multiple rows with the same post
### in the output.
###
### This query requires joining three tables: Posts, Comments, and PostTypes.
###
### Output: Id (Posts), Title, Text (Comments)
### Order by: Id ascending
queries[10] = """
select 0;
"""


### 11. For the users who have received at least 200 badges in total, find the
### number of badges they have received in each year. This can be used, e.g., to 
### create a plot of the number of badges received in each year for the most active users.
###
### There should be an entry for a user for every year in which badges were given out.
###
### We have provided some WITH clauses to help you get started. You may wish to 
### add more (or modify these).
###
### Output columns: Id, DisplayName, Year, Num_Badges
### Order by Id ascending, Year ascending
queries[11] = """
with years as (
        select distinct extract(year from date) as year 
        from badges),
     temp1 as (
        select id, displayname, year
        from users, years
        where id in (select userid from badges group by userid having count(*) >= 200)
     )
select 0;
"""

### 12. Find the post(s) that took the longest to answer, i.e., the gap between its creation date
### and the creation date of the first answer to it (in number of days). Ignore the posts with no
### answers. Keep in mind that "AcceptedAnswerId" is the id of the post that was marked
### as the answer to the question -- joining on "parentid" is not the correct way to find the answer.
###
### Hint: Use with to create an appropriate table first.
###
### Output columns: Id, Title, Gap
queries[12] = """
select 0;
"""


### 13. Write a query to find the posts with at least 7 children, i.e., at
### least 7 other posts have that post as the parent
###
### Output columns: Id, Title
### Order by: Id ascending
queries[13] = """
select 0;
"""

### 14. Find posts such that, between the post and its children (i.e., answers
### to that post), there are a total of 100 or more votes
###
### HINT: Use "union all" to create an appropriate temp table using WITH
###
### Output columns: Id, Title
### Order by: Id ascending
queries[14] = """
select 0;
"""

### 15. Let's see if there is a correlation between the length of a post and the score it gets.
### We don't have posts in the database, so we will do this on title instead.
### Write a query to find the average score of posts for each of the following ranges of post title length:
### 0-9 (inclusive), 10-19, ...
###
### We will ignore the posts with no title.
###
### HINT: Use the "floor" function to create the ranges.
###
### Output columns: Range_Start, Range_End, Avg_Score
### Order by: Range ascending
queries[15] = """
select 0;
"""


### 16. Write a query to generate a table: 
### (VoteTypeDescription, Day_of_Week, Num_Votes)
### where we count the number of votes corresponding to each combination
### of vote type and Day_of_Week (obtained by extract "dow" on CreationDate).
### So Day_of_Week will take values from 0 to 6 (Sunday to Saturday resp.)
###
### Don't worry if a particular combination of Description and Day of Week has 
### no votes -- there should be no row in the output for that combination.
###
### Output column order: VoteTypeDescription, Day_of_Week, Num_Votes
### Order by VoteTypeDescription asc, Day_of_Week asc
queries[16] = """
select 0;
"""
