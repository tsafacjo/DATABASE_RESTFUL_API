# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request 
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt 
 
app = Flask(__name__)
api = Api(app) 
client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db['Users']

def verifyPw(username, password):
    hashed_pw = users.find({
            "Username":username
            })[0]["Password"]
    if bcrypt.hashpw(password.encode("utf-8"), hashed_pw) == hashed_pw:
        return True 
    else :
        return False
def countTokens(username):     
    tokens = users.find({"Username":username})[0]["Tokens"]
    return tokens           
            
class Register(Resource):
    def post(self):   
        posted_data = request.get_json()
        # Get the data 
        username = posted_data["username"]
        password = posted_data["password"]
        #hash 
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        #store username and password into the database
        users.insert({
                "Username":username,
                "Password":hashed_password,
                "Tokens":10,
                "Sentence":""
                })
        retJson = {
                "status":200,
                "msg":"You succesfully signed up for the API"
                }
        return jsonify(retJson)

class Store(Resource):
      def post(self):
         # step 1 get the posted data 
          posted_data= request.get_json()
         # collect data from posted data
          username = posted_data["username"]
          password = posted_data["password"]
          sentence = posted_data["Sentence"]
          #Step 3
          correct_pw =  verifyPw(username, password)
          if not correct_pw:
              retJson = {
                      "status":302
                      }
              return jsonify(retJson)
          num_tokens = countTokens(username)
          if num_tokens <= 0:
              retJson = {
                      "status":301
                      }
              return jsonify(retJson)
          
          users.update({
                  "Username":username
                  }, {"$set":{"Sentence":sentence,
                                  
                              "Token": num_tokens-1}})
          retJson = {
                  "status":200,
                  "msg": "Sentence saved successfully"
                  }    
          return (retJson)
      
class Read(Resource):
      def post(self):
         # step 1 get the posted data 
          posted_data= request.get_json()
         # collect data from posted data
          username = posted_data["username"]
          password = posted_data["password"]
          #Step 3
          correct_pw =  verifyPw(username, password)
          if not correct_pw:
              retJson = {
                      "status":302
                      }
              return jsonify(retJson)
          num_tokens = countTokens(username)
          if num_tokens <= 0:
              retJson = {
                      "status":301
                      }
              return jsonify(retJson)
          
          sentence = users.find({
            "Username":username
            })[0]["Sentence"]
          retJson = {
                  "status":200,
                  "msg": sentence
                  }    
          return (retJson)
    

api.add_resource(Register, "/register")
api.add_resource(Store, "/store")
api.add_resource(Read, "/read")
   
if __name__ == "__main__":
    app.run(host = "0.0.0.0",debug= True)