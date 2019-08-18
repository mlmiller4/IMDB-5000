from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import IMDB
import pandas as pd, numpy as np
import json

app = Flask(__name__)
api = Api(app)

actors = [
    {
        "last name": "Ford",
        "full name": "Harrison Ford",
        "facebook likes": 11000
    },
    {
        "last name": "Hanks",
        "full name": "Tom Hanks",
        "facebook likes": 15000
    },
    {
        "last name": "Lawrence",
        "full name": "Jennifer Lawrence",
        "facebook likes": 34000
    },
    {
        "last name": "Cruise",
        "full name": "Tom Cruise",
        "facebook likes": 10000
    },
    {
        "last name": "Pattinson",
        "full name": "Robert Pattinson",
        "facebook likes": 21000
    },
    {
        "last name": "Cooper",
        "full name": "Bradley Cooper",
        "facebook likes": 14000
    },
    {
        "last name": "Hemsworth",
        "full name": "Chris Hemsworth",
        "facebook likes": 26000
    },
    {
        "last name": "Williams",
        "full name": "Robin Williams",
        "facebook likes": 49000
    },
    {
        "last name": "Simmons",
        "full name": "J.K. Simmons",
        "facebook likes": 24000
    },
    {
        "last name": "DiCaprio",
        "full name": "Leonardo DiCaprio",
        "facebook likes": 29000
    }
]

class Actor(Resource):

    def get(self, lastName):
        for actor in actors:
            if(lastName == actor['last name']):
                return actor, 200
        return "Actor not found", 404

    def post(self, lastName):
        parser = reqparse.RequestParser()
        parser.add_argument("full name")
        parser.add_argument("facebook likes")
        args = parser.parse_args()

        for actor in actors:
            if(lastName == actor["last name"]):
                return "Actor with name {} already exists".format(lastName), 400

        actor = {
            "last name": lastName,
            "full name": args["full name"],
            "facebook likes": args["facebook likes"]
        }

        actors.append(actor)
        return actor, 201

    def put(self, lastName):
        parser = reqparse.RequestParser()
        parser.add_argument("full name")
        parser.add_argument("facebook likes")
        args = parser.parse_args()

        for actor in actors:
            if(lastName == actor["last name"]):
                actor["full name"] = args["full name"]
                actor["facebook likes"] = args["facebook likes"]
                return actor, 200

        actor = {
            "last name": lastName,
            "full name": args["full name"],
            "facebook likes": args["facebook likes"]
        }

        actors.append(actor)
        return actor, 201

    def delete(self, lastName):
        global actors
        actors = [actor for actor in actors if actor['last name'] != lastName]
        return "{} is deleted".format(lastName), 200

api.add_resource(Actor, "/actor/<string:lastName>")
app.run(debug=True)



# if __name__ == '__main__':
#     app.run(debug=True)