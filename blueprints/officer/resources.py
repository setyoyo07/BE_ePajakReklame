from flask_restful import Resource, Api, marshal
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, officer_required, surveyor_required
from blueprints.officer.model import Officer
from blueprints.daerah.model import Daerah

blueprint_officer = Blueprint("officer", __name__)
api_officer = Api(blueprint_officer)

class OfficerResources(Resource):
    """
    Class yang digunakan untuk mengakomodasi aktivitas Officer

    Methods
    -------
    options(id=None)
        Return status ok ketika API ditembak
    get
        Return Data informasi dari Officer
    """
    def options(self, id=None):
        return {'status':'ok'},200

    #mengambil data officer (data diri untuk user (officer) yg sedang login)
    @jwt_required
    @officer_required
    def get(self): 
        """
        Fungsi untuk mengambil (get) data informasi mengenai officer

        Response
        --------
        id : int
          id dari officer, diambil dari database  
        nip : str
          nomor induk pegawai milik officer, diambil dari database
        nama : str
          nama officerer, diambil dari database
        nama_daerah : str
          nama daerah (Kota/Kabupaten) tempat officer bekerja, diambil dari database
        """ 
        data_claims = get_jwt_claims()
        officer = Officer.query.get(data_claims["id"])
        daerah = Daerah.query.get(officer.daerah_id)
        marshalOfficer = marshal(officer, Officer.response_fields)
        marshalOfficer["nama_daerah"] = daerah.nama
        return [marshalOfficer], 200, {"Content-Type": "application/json"}

class SurveyorResources(Resource):
    """
    Class yang digunakan untuk mengakomodasi aktivitas Surveyor

    Methods
    -------
    options(id=None)
        Return status ok ketika API ditembak
    get
        Return Data informasi dari Surveyor
    """
    def options(self, id=None):
        return {'status':'ok'},200

    #mengambil data surveyor (data diri untuk user (surveyor) yg sedang login)
    @jwt_required
    @surveyor_required
    def get(self):
        """
        Fungsi untuk mengambil (get) data informasi mengenai surveyor

        Response
        --------
        id : int
          id dari surveyor, diambil dari database  
        nip : str
          nomor induk pegawai milik surveyor, diambil dari database
        nama : str
          nama surveyor, diambil dari database
        nama_daerah : str
          nama daerah (Kota/Kabupaten) tempat surveyor bekerja, diambil dari database
        """ 
        data_claims = get_jwt_claims()
        officer = Officer.query.get(data_claims["id"])
        daerah = Daerah.query.get(officer.daerah_id)
        marshalOfficer = marshal(officer, Officer.response_fields)
        marshalOfficer["nama_daerah"] = daerah.nama
        return [marshalOfficer], 200, {"Content-Type": "application/json"}

api_officer.add_resource(OfficerResources, "")
api_officer.add_resource(SurveyorResources, "/surveyor")
