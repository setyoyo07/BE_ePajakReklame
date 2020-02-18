from flask_restful import Resource, Api, marshal
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, payer_required
from blueprints.payer.model import Payer
from blueprints.daerah.model import Daerah

blueprint_payer = Blueprint("payer", __name__)
api_payer = Api(blueprint_payer)

class PayerResources(Resource):
    """
    A class used to contain Payer's action to Get payer info data

    Methods
    -------
    options(id=None)
        Return status ok when get hit
    get
        Return payer info data
    """
    def options(self, id=None):
        return {'status':'ok'},200

    @jwt_required
    @payer_required
    def get(self): 
        """
        Get payer info data

        Response
        --------
        id = int
        npwpd = str
        nama = str
        nama_usaha = str
        alamat_usaha = str
        nama_daerah = str
        """
        data_claims = get_jwt_claims()
        payer = Payer.query.get(data_claims["id"])
        daerah = Daerah.query.get(payer.daerah_id)
        marshalPayer = marshal(payer, Payer.response_fields)
        marshalPayer["nama_daerah"] = daerah.nama 
        return [marshalPayer], 200, {"Content-Type": "application/json"}

api_payer.add_resource(PayerResources, "")
