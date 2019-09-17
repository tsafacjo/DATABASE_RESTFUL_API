# -*- coding: utf-8 -*-
from flask import Flask, jsonify, request 
from flask_restful import Api, Resource 
app = Flask(__name__)

api = Api(app) 

def checkPosted_data(posted_data, function_name):
    if(function_name == "add"):
        if "x" not in posted_data or  "y" not in posted_data :
                return 301    
        else:
            return 200
    
class Add(Resource):
    def post(self):
        #If I 'm here, then the resource Add was requested using the method POST
        posted_data = request.get_json()
        status_code = checkPosted_data(posted_data, "add")
        if(status_code == 301):
            retJson= {
                    "Message":"An error happened",
                    "Status Code":status_code
                    }
            return jsonify(retJson)
        x = posted_data["x"]
        y = posted_data["y"]
        x = int(x)
        y = int(y)
        ret = x+y
        # Step 2: Add the posted data 
        retMap = {
                "Message":ret,
                "Status Code":200
                }
        return jsonify(retMap)

class Subtract(Resource):
    pass

class Multiply(Resource):
    pass
    

api.add_resource(Add, "/add")
   
if __name__ == "__main__":
    app.run(debug= True)