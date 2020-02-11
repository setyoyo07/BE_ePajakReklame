from flask_restful import Resource, Api, reqparse, marshal
from flask import Blueprint
from blueprints import db, app, payer_required
from .model import *
from flask_jwt_extended import jwt_required, get_jwt_claims, verify_jwt_in_request

blueprint_variabel_perhitungan = Blueprint("variabel_perhitungan", __name__)
api = Api(blueprint_variabel_perhitungan)

#Resource model variabel perhitungan untuk keperluan input form
class PayerVariabelPerhitunganResource(Resource):
    # fungsi untuk handle CORS
    def options(self, id=None):
        return 200

    #fungsi untuk mengambil data variabel perhitungan yang diperlukan untuk membuat form input
    @jwt_required
    @payer_required
    def get(self):
        variabel_perhitungan = VariabelPerhitungan.query
        
        list_tarif_tambahan = []
        for tarif_tambahan in variabel_perhitungan.filter_by(kata_kunci_induk = 'TTM').all() :
            list_tarif_tambahan.append(tarif_tambahan.nama)
        list_reklame_permanen = []
        for reklame_permanen in variabel_perhitungan.filter_by(kata_kunci_induk = 'JR-RP').all():
            list_reklame_permanen.append(reklame_permanen.nama)
        list_reklame_non_permanen = []
        for reklame_non_permanen in variabel_perhitungan.filter_by(kata_kunci_induk = 'JR-RNP').all() :
            list_reklame_non_permanen.append(reklame_non_permanen.nama)
        list_letak_pemasangan = []
        for letak_pemasangan in variabel_perhitungan.filter_by(kata_kunci_induk = 'FR').all() :
            list_letak_pemasangan.append(letak_pemasangan.nama)    
        list_klasifikasi_jalan = []
        for klasifikasi_jalan in variabel_perhitungan.filter_by(kata_kunci_induk = 'FJ').all() :
            list_klasifikasi_jalan.append(klasifikasi_jalan.nama)
        list_sudut_pandang = []
        for sudut_pandang in variabel_perhitungan.filter_by(kata_kunci_induk = 'FSP').all() :
            list_sudut_pandang.append(sudut_pandang.nama)

        hasil = {
            "list_tarif_tambahan": list_tarif_tambahan,
            "list_reklame_permanen": list_reklame_permanen,
            "list_reklame_non_permanen": list_reklame_non_permanen,
            "list_letak_pemasangan":list_letak_pemasangan,
            "list_klasifikasi_jalan":list_klasifikasi_jalan,
            "list_sudut_pandang": list_sudut_pandang
        }
        return hasil, 200, {'Content-Type': 'application/json'}

api.add_resource(PayerVariabelPerhitunganResource, '/payer')