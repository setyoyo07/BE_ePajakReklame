from flask_restful import Resource, Api, marshal
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, officer_required, surveyor_required
from blueprints.officer.model import Officer
from blueprints.daerah.model import Daerah

blueprint_officer = Blueprint("officer", __name__)
api_officer = Api(blueprint_officer)

#Resource model database officer untuk mengambil data officer
class OfficerResources(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return {'status':'ok'},200

    #mengambil data officer (data diri untuk user (officer) yg sedang login)
    @jwt_required
    @officer_required
    def get(self): 
        data_claims = get_jwt_claims()
        officer = Officer.query.get(data_claims["id"])
        daerah = Daerah.query.get(officer.daerah_id)
        marshalOfficer = marshal(officer, Officer.response_fields)
        marshalOfficer["nama_daerah"] = daerah.nama
        return [marshalOfficer], 200, {"Content-Type": "application/json"}

#Resource model database officer untuk mengambil data surveyor
class SurveyorResources(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return {'status':'ok'},200

    #mengambil data surveyor (data diri untuk user (surveyor) yg sedang login)
    @jwt_required
    @surveyor_required
    def get(self): 
        data_claims = get_jwt_claims()
        officer = Officer.query.get(data_claims["id"])
        daerah = Daerah.query.get(officer.daerah_id)
        marshalOfficer = marshal(officer, Officer.response_fields)
        marshalOfficer["nama_daerah"] = daerah.nama
        return [marshalOfficer], 200, {"Content-Type": "application/json"}

api_officer.add_resource(OfficerResources, "")
api_officer.add_resource(SurveyorResources, "/surveyor")
