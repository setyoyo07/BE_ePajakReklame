from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token
from blueprints.officer.model import *
from blueprints.payer.model import *
import hashlib

blueprint_auth = Blueprint("auth", __name__)
api = Api(blueprint_auth)

#resource untuk fitur login
class CreateTokenResources(Resource):
    #untuk handle cors
    def options(self, id=None):
        return {'status':'ok'}, 200
    
    #buat token user
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("nip", location="json", required=False, default="")
        parser.add_argument("npwpd", location="json", required=False, default="")
        parser.add_argument("pin", location="json", required=True)
        args = parser.parse_args()
        pin_hashlib = hashlib.md5(args["pin"].encode()).hexdigest()

        # jika yang login adalah officer
        if args["nip"] != "" and args["npwpd"] == "":
            list_officer = Officer.query.filter_by(nip=args['nip']).filter_by(pin=pin_hashlib)
            user_claims_data = list_officer.first()
            if user_claims_data is None:
                return {"message": "NIP not match"}, 404
            else : 
                user_claims_data = marshal(user_claims_data, Officer.jwt_claim_fields)
                token = create_access_token(identity=user_claims_data['nip'], user_claims=user_claims_data)
                user_claims_data['token'] = token
                return {"token": token, "message": "Token is successfully created"}, 200, {"Content-Type": "application/json"}
        # jika yang login adalah payer
        else:
            list_payer = Payer.query.filter_by(npwpd=args['npwpd']).filter_by(pin=pin_hashlib)
            user_claims_data = list_payer.first()
            user_claims_data = marshal(user_claims_data, Payer.jwt_claim_fields)
            user_claims_data['role'] = "payer" 
            if user_claims_data['npwpd'] != None:
                token = create_access_token(identity=user_claims_data['npwpd'], user_claims=user_claims_data)
                user_claims_data['token'] = token
                return {"token": token, "message": "Token is successfully created"}, 200, {"Content-Type": "application/json"}
            else:
                return {'message': 'NPWPD not match'}, 404


api.add_resource(CreateTokenResources, "/")
