from flask_restful import Resource, Api, marshal
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, payer_required
from blueprints.payer.model import Payer
from blueprints.daerah.model import Daerah

blueprint_payer = Blueprint("payer", __name__)
api_payer = Api(blueprint_payer)

#Resource model database payer untuk mengambil data payer
class PayerResources(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return {'status':'ok'},200

    #mengambil data payer (data diri untuk user (payer) yg sedang login)
    @jwt_required
    @payer_required
    def get(self): 
        data_claims = get_jwt_claims()
        payer = Payer.query.get(data_claims["id"])
        daerah = Daerah.query.get(payer.daerah_id)
        marshalPayer = marshal(payer, Payer.response_fields)
        marshalPayer["nama_daerah"] = daerah.nama 
        return [marshalPayer], 200, {"Content-Type": "application/json"}

api_payer.add_resource(PayerResources, "")
