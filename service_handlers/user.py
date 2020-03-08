from flask_restful import Resource
from flask import request 
from jsonschema import validate

from database_access.user import get_user_by_id, get_all_user, get_user_by_mail, create_user
from database_access.session import get_session

class User(Resource):

    def __init__(self):
        self.basic_schema = {
            "type" : "object",
            "properties" : {
                "username" : {"type" : "string"},
                "email" : {
                    "type" : "string",
                    "pattern": "^[_A-Za-z0-9-\\+]+(\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9-]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})$",
                },
                "password" : {"type" : "string"},
                "first_name" : {"type" : "string"},
                "middle_name" : {"type" : "string"},
                "last_name" : {"type" : "string"},
                "mobile_number" : {
                    "type" : "string",
                    "pattern": "^[6-9][0-9]{9}$",
                },
            }
        }

        self.update_personal_details_schema = {
            "type" : "object",
            "properties" : {
                "gender" : {
                    "type" : "string",
                    "enum" : ["Male", "Female", "Other"]
                },
                "dob" : {
                    "type" : "string"
                },
                "height" : {
                    "type" : "object"
                    "properties" : {
                        "unit" : {"type" : "string"},
                        "value" : {"type" : "number"}
                    }
                },
                "weight" : {
                    "type" : "object"
                    "properties" : {
                        "unit" : {"type" : "string"},
                        "value" : {"type" : "number"}
                    }
                }
            },
            "required" : ["gender"]
        }

        self.address_schema = {
            "type" : "object",
            "properties" : {
                "full_name" : {"type" : "string"},
                "mobile_number" : {
                    "type" : "string",
                    "pattern": "^[6-9][0-9]{9}$"
                },
                "address_line_1" : {"type" : "string"},
                "address_line_2" : {"type" : "string"},
                "landmark" : {"type" : "string"},
                "city" : {"type" : "string"},
                "state" : {"type" : "string"},
                "pincode" :  : {
                    "type" : "string",
                    "pattern" : "^[1-9][0-9]{5}$"
                }
                "latitude" : {"type" : "string"},
                "longitute" : {"type" : "string"}
            }
            "required" : ["full_name", "mobile_number", "address_line_1", "address_line_2", "city", "state", "pincode"]
        }

    def __validate(self,payload,schema):
        try:
            validate(payload,schema)
            return True
        except:
            return False
    

    # def __single(self,user_object):
    #     return {
    #         "userId" : str(user_object["_id"]),
    #         "email" : user_object.get("email","No Email Address"),
    #         "name" : user_object.get("name","Default Name")
    #     }

    # def __multiple(self,user_objects):
    #     return [ self.__single(user_object) for user_object in user_objects ]


    def get(self):
        params = request.args.to_dict()
        session = get_session(params['token'])
        current_user_id = str(session['user'])
        if current_user_id:
            user = get_user_by_id(current_user_id)
            if not user:
                return {
                    "response" : None,
                    "messege" : "Invalid Token",
                    "status": False
                }, 404  
            return {
                "response" : self.__single(user),
                "messege" : "Ok",
                "status": True
            },200


    def post(self):
        payload = request.json
        if not self.__validate_user(payload):
            return {
                "response" : None,
                "messege" : "Invalid Email or Password ",
                "status": False
            }, 401    

        email = payload['email']
        user = get_user_by_mail(email)
        if user:
            return {
                "response" : None,
                "messege" : "User Already Exist with this Email",
                "status" : False
            }, 401

        create_user(payload)
        user = get_user_by_mail(email)
        return {
            "response" : None,
            "messege" : "User created Successfully",
            "status" : True
        }, 200
