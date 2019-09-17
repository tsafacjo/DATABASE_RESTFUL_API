# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request 
from flask_restful import Api, Resource
from pymongo import MongoClient
 
app = Flask(__name__)
api = Api(app) 
client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db['UserNum']
UserNum.insert({
        "num_of_users":0
        })

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]["num_of_users"]
        new_num = prev_num + 1
        UserNum.update({},{"$set":{"num_of_users":new_num}})
        return "Hello new user "+str(new_num)

api.add_resource(Visit, "/hello")
   
if __name__ == "__main__":
    app.run(host = "0.0.0.0",debug= True)