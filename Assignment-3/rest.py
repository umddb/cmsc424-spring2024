from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
api = Api(app)
CORS(app)

class Post(Resource):
    def get(self, postid):
        #####################################################################################3
        #### Important -- This is the how the connection must be done for autograder to work
        ### But on your local machine, you may need to remove "host=..." part if this doesn't work
        #####################################################################################3
        conn = psycopg2.connect("host=127.0.0.1 dbname=stackexchange user=root password=root")
        cur = conn.cursor()

        cur.execute("select id, posttypeid, title, AcceptedAnswerID, creationdate from posts where id = %s" % (postid))
        ans = cur.fetchall()
        if len(ans) == 0:
            return "Post Not Found", 404
        else:
            ret = {"id": ans[0][0], "PostTypeID": ans[0][1], "Title": str(ans[0][2]), "AcceptedAnswerID": str(ans[0][3]), "CreationDate": str(ans[0][4])}
            return ret, 200


class Dashboard(Resource):
    # Return some sort of a summary of the data -- we will use the "name" attribute to decide which of the dashboards to return
    # 
    # Here the goal is to return the top 100 users using the reputation -- this will be returned as an array in increasing order of Rank
    # Use PostgreSQL default RANK function (that does sparse ranking), followed by a limit 100 to get the top 100 
    #
    # FORMAT: {"Top 100 Users by Reputation": [{"ID": "...", "DisplayName": "...", "Reputation": "...", "Rank": "..."}, {"ID": "...", "DisplayName": "...", "Reputation": "...", "Rank": "..."}, ]
    def get(self, name):
        if name == "top100users":
            return "Not implemented yet", 404
        else:
            return "Unknown Dashboard Name", 404

class User(Resource):
    # Return all the info about a specific user, including the titles of the user's posts as an array
    # The titles array must be sorted in the increasing order by the title.
    # Remove NULL titles if any
    # FORMAT: {"ID": "...", "DisplayName": "...", "CreationDate": "...", "Reputation": "...", "PostTitles": ["posttitle1", "posttitle2", ...]}
    def get(self, userid):
        # Add your code to construct "ret" using the format shown below
        # Post Titles must be sorted in alphabetically increasing order
        # CreationDate should be of the format: "2007-02-04" (this is what Python str() will give you)

        # Add your code to check if the userid is already present in the database
        exists_user = True

        if not exists_user:
            return "User not found", 404
        else:
            ret = {"ID": "xyz", "DisplayName": "xyz", "CreationDate": "...", "Reputation": "...", "PostTitles": ["posttitle1", "posttitle1"]}
            return ret, 200

    # Add a new user into the database, using the information that's part of the POST request
    # We have provided the code to parse the POST payload
    # If the "id" is already present in the database, a FAILURE message should be returned
    def post(self, userid):
        parser = reqparse.RequestParser()
        parser.add_argument("reputation")
        parser.add_argument("creationdate")
        parser.add_argument("displayname")
        parser.add_argument("upvotes")
        parser.add_argument("downvotes")
        args = parser.parse_args()
        print("Data received for new user with id {}".format(userid))
        print(args)

        # Add your code to check if the userid is already present in the database
        exists_user = True

        if exists_user:
            return "FAILURE -- Userid must be unique", 201
        else:
            # Add your code to insert the new tuple into the database
            return "SUCCESS", 201

    # Delete the user with the specific user id from the database
    def delete(self, userid):
        # Add your code to check if the userid is present in the database
        exists_user = False

        if exists_user:
            # Add your code to delete the user from the user table
            # If there are corresponding entries in "badges" table for that userid, those should be deleted
            # For posts, comments, votes, set the appropriate userid fields to -1 (since that content should not be deleted)
            return "SUCCESS", 201
        else:
            return "FAILURE -- Unknown Userid", 404
      
api.add_resource(User, "/user/<int:userid>")
api.add_resource(Post, "/post/<int:postid>")
api.add_resource(Dashboard, "/dashboard/<string:name>")

app.run(debug=True, host="0.0.0.0", port=5000)
