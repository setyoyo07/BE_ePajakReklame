from flask_restful import Resource, Api, reqparse, marshal
from flask import Blueprint
from sqlalchemy import desc
from blueprints import db, app, payer_required
from blueprints.payer.model import Payer
from blueprints.objek_pajak.model import ObjekPajak
from blueprints.bukti_pembayaran.model import BuktiPembayaran
from flask_jwt_extended import jwt_required, get_jwt_claims, verify_jwt_in_request

blueprint_objek_pajak = Blueprint("objek_pajak", __name__)
api = Api(blueprint_objek_pajak)

#Resource model objek pajak oleh payer
class ObjekPajakResource(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return 200

    #fungsi untuk menambah objek pajak baru serta menghitung laporan / total pajak yang harus dibayar
    @jwt_required
    @payer_required
    def post(self):
        verify_jwt_in_request() 
        payer_claims_data = get_jwt_claims()
        payer = Payer.query.get(payer_claims_data["id"])
        parser = reqparse.RequestParser()
        parser.add_argument('nama_reklame', location='json', required=True)
        parser.add_argument('judul_reklame', location='json', required=True)
        parser.add_argument('tipe_reklame', location='json', required=True)
        parser.add_argument('jenis_reklame', location='json', required=True)
        parser.add_argument('foto', location='json', required=True)
        parser.add_argument('panjang', type=int, location='json', required=True)
        parser.add_argument('lebar', type=int, location='json', required=True)
        parser.add_argument('tinggi', type=int, location='json', required=True)
        parser.add_argument('jumlah', type=int, location='json', required=True)
        parser.add_argument('muka', type=int, location='json', required=True)
        parser.add_argument('luas', type=int, location='json', required=True)
        parser.add_argument('tanggal_pemasangan', location='json', required=True)
        parser.add_argument('tanggal_pembongkaran', location='json', required=True)
        parser.add_argument('masa_pajak', location='json', required=True)
        parser.add_argument('lokasi', location='json', required=True)
        parser.add_argument('longitude', location='json', required=True)
        parser.add_argument('latitude', location='json', required=True)
        parser.add_argument('tarif_tambahan', location='json', required=True)
        parser.add_argument('letak_pemasangan', location='json', required=True)
        parser.add_argument('klasifikasi_jalan', location='json', required=True)
        parser.add_argument('sudut_pandang', location='json', required=True)
        args = parser.parse_args()

        get_id = ObjekPajak.query.order_by(desc('id')).first()
        if get_id is None:
            nopd = "1001"
        else :
            nopd = str(1000+get_id.id)

        # menambah data objek pajak baru
        objek_pajak = BuktiPembayaran(
            payer.id, nopd, args["nama_reklame"], args["judul_reklame"], args["tipe_reklame"],
            args["jenis_reklame"], args["foto"], args["panjang"], args["lebar"], args["tinggi"],
            args["jumlah"], args["tangal_pemasangan"], args["tanggal-pembongkaran"], args["longitude"],
            args["masa_pajak"], args["latitude"], args["lokasi"], args["muka"], args['luas'], args["tarif_tambahan"],
            args["letak_pemasangan"], args["klasifikasi_jalan"], args["sudut_pandang"]
            )
        db.session.add(objek_pajak)
        db.session.commit()
        app.logger.debug('DEBUG : %s', objek_pajak)
            
        #perhitungan total pajak yang harus dibayar oleh payer
        # nilai luas reklame
        if args["tipe_reklame"] == "permanen" :
            if args["luas"] <= 3 :
                
        else :


        return {"message": "Pembayaran sukses", "nomor_sspd": bukti_pembayaran.nomor_sspd}, 200, {'Content-Type': 'application/json'}

api.add_resource(ObjekPajakResource, '/payer')