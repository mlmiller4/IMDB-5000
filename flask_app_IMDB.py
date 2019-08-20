from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import IMDB
import pandas as pd, numpy as np
import json

app = Flask(__name__)
api = Api(app)

# Load the movie_metadata.csv and get the top 10 most profitable actors
appDF = pd.read_csv("movie_metadata.csv")
appDF = IMDB.calculateProfit(appDF)
actorsDF = IMDB.get_columns(appDF, ['actor_1_name','profit'])
top10actors = IMDB.top10(actorsDF, 'actor_1_name', 'profit', 'sum')

del top10actors['sum_profit']               # don't need profit info
top10actors.columns = ['name']
top10actors['facebook likes'] = 0
top10actors['unspacedName'] = top10actors['name'].str.replace(' ','')   # Create column for actor name with no spaces

# Add in number of facebook likes data
for index, row in top10actors.iterrows():
    matchingRow = appDF[appDF['actor_1_name'] == row['name']].iloc[0]
    top10actors.at[index, 'facebook likes'] = matchingRow['actor_1_facebook_likes']

top10actors = top10actors.reset_index(drop=True)    # reset index

# Data must be formatted as a series of dictionaries where 'name','facebook likes', and 'unspacedName' are keys
actors = top10actors.to_dict('records')


''' test data - not used when accessing data through IMDB functions '''
# actors = [
#     {
#         "last name": "Ford",
#         "full name": "Harrison Ford",
#         "facebook likes": 11000
#     },
#     {
#         "last name": "Hanks",
#         "full name": "Tom Hanks",
#         "facebook likes": 15000
#     },
#     {
#         "last name": "Lawrence",
#         "full name": "Jennifer Lawrence",
#         "facebook likes": 34000
#     },
#     {
#         "last name": "Cruise",
#         "full name": "Tom Cruise",
#         "facebook likes": 10000
#     },
#     {
#         "last name": "Pattinson",
#         "full name": "Robert Pattinson",
#         "facebook likes": 21000
#     },
#     {
#         "last name": "Cooper",
#         "full name": "Bradley Cooper",
#         "facebook likes": 14000
#     },
#     {
#         "last name": "Hemsworth",
#         "full name": "Chris Hemsworth",
#         "facebook likes": 26000
#     },
#     {
#         "last name": "Williams",
#         "full name": "Robin Williams",
#         "facebook likes": 49000
#     },
#     {
#         "last name": "Simmons",
#         "full name": "J.K. Simmons",
#         "facebook likes": 24000
#     },
#     {
#         "last name": "DiCaprio",
#         "full name": "Leonardo DiCaprio",
#         "facebook likes": 29000
#     }
# ]

class Actor(Resource):

    def get(self, unspacedName):
        for actor in actors:
            if unspacedName == actor['unspacedName']:
                return actor, 200
        return 'Actor not found', 404


    def post(self, unspacedName):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("facebook likes")
        args = parser.parse_args()

        for actor in actors:
            if(unspacedName == actor['unspacedName']):
                return "Actor with the name {} already exists".format(actor['name']), 400

        actor = {
            "unspacedName": unspacedName,
            "name": args["name"],
            "facebook likes": args["facebook likes"]
        }

        actors.append(actor)
        return actor, 201

    def put(self, unspacedName):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("facebook likes")
        args = parser.parse_args()

        # Update info if the actor is already present
        for actor in actors:
            if(unspacedName == actor["unspacedName"]):
                actor["name"] = args["name"]
                actor["facebook likes"] = args["facebook likes"]
                return actor, 200

        # If actor is not already present, append new actor info
        actor = {
            "unspacedName": unspacedName,
            "name": args["name"],
            "facebook likes": args["facebook likes"]
        }

        actors.append(actor)
        return actor, 201

    def delete(self, unspacedName):
        global actors
        actors = [actor for actor in actors if actor['unspacedName'] != unspacedName]
        return "{} is deleted".format(unspacedName), 200

api.add_resource(Actor, "/actor/<string:unspacedName>")
app.run(debug=True)



# if __name__ == '__main__':
#     app.run(debug=True)