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
    Class yang digunakan untuk mengakomodasi aktivitas Payer

    Methods
    -------
    options(id=None)
        Return status ok ketika API ditembak
    get
        Return Data informasi dari Payer
    """
    def options(self, id=None):
        return {'status':'ok'},200

    @jwt_required
    @payer_required
    def get(self): 
        """
        Fungsi untuk mengambil (get) data informasi mengenai payer

        Response
        --------
        id : int
          id dari payer, diambil dari database  
        npwpd : str
          nomor pokok wajib pajak daerah milik payer, diambil dari database
        nama : str
          nama payer, diambil dari database
        nama_usaha : str
          nama usaha milik payer, diambil dari database
        alamat_usaha : str
          alamat usaha milik payer, diambil dari database
        nama_daerah : str
          nama daerah (Kota/Kabupaten) tempat payer memasang pajak reklame, diambil dari database
        """
        data_claims = get_jwt_claims()
        payer = Payer.query.get(data_claims["id"])
        daerah = Daerah.query.get(payer.daerah_id)
        marshalPayer = marshal(payer, Payer.response_fields)
        marshalPayer["nama_daerah"] = daerah.nama 
        return [marshalPayer], 200, {"Content-Type": "application/json"}

api_payer.add_resource(PayerResources, "")
