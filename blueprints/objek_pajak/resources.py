from flask_restful import Resource, Api, reqparse, marshal
from flask import Blueprint
from sqlalchemy import desc
from blueprints import db, app, payer_required
from blueprints.payer.model import Payer
from blueprints.objek_pajak.model import ObjekPajak
from blueprints.laporan.model import Laporan
from blueprints.variabel_perhitungan.model import VariabelPerhitungan
from flask_jwt_extended import jwt_required, get_jwt_claims, verify_jwt_in_request
from datetime import datetime
import math

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
        parser.add_argument('panjang', type=float, location='json', required=True)
        parser.add_argument('lebar', type=float, location='json', required=True)
        parser.add_argument('tinggi', type=float, location='json', required=True)
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
        parser.add_argument('jangka_waktu_pajak', location='json', required=True)

        args = parser.parse_args()

        get_id = ObjekPajak.query.order_by(desc('id')).first()
        if get_id is None:
            nopd = "1001"
        else :
            nopd = str(1000+get_id.id+1)

        # menambah data objek pajak baru
        objek_pajak = ObjekPajak(
            payer.id, nopd, args["nama_reklame"], args["judul_reklame"], args["tipe_reklame"],
            args["jenis_reklame"], args["foto"], args["panjang"], args["lebar"], args["tinggi"],
            args["jumlah"], args["tanggal_pemasangan"], args["tanggal_pembongkaran"], args["masa_pajak"],
            args["longitude"], args["latitude"], args["lokasi"], args["muka"], args['luas'], args["tarif_tambahan"],
            args["letak_pemasangan"], args["klasifikasi_jalan"], args["sudut_pandang"], args["jangka_waktu_pajak"]
            )
        db.session.add(objek_pajak)
        db.session.commit()
        app.logger.debug('DEBUG : %s', objek_pajak)
            
        variabel_perhitungan = VariabelPerhitungan.query
        #perhitungan total pajak yang harus dibayar oleh payer
        #tarif tambahan
        TTM = variabel_perhitungan.filter_by(nama = args["tarif_tambahan"]).first()
        TTM = TTM.nilai

        #nilai ketinggian reklame (NKR)
        jenis_reklame = variabel_perhitungan.filter_by(nama = args["jenis_reklame"]).first()
        HDKR = variabel_perhitungan.filter_by(kata_kunci = ("HDKR-"+jenis_reklame.kata_kunci)).first()
        NKR = args["tinggi"] * HDKR.nilai * (1 + TTM)

        if args["tipe_reklame"] == "Reklame Permanen" :    
            # harga dasar ukuran reklame (HDUR)
            if args["luas"] <= 10 :
                kode_luas = "-0"
            elif args["luas"] > 50 :
                kode_luas = "-50"
            else :
                kode_luas = "-10"
            HDUR = variabel_perhitungan.filter_by(kata_kunci=("HDUR-"+jenis_reklame.kata_kunci + kode_luas)).first()

            # harga dasar nilai strategis pemasangan reklame (HDNSPR)
            if args["luas"] < 3 :
                kode_luas = "-0"
            elif args["luas"] < 10 :
                kode_luas = "-3"
            elif args["luas"] <= 50 :
                kode_luas = "-10"
            else :
                kode_luas = "-50"
            HDNSPR = variabel_perhitungan.filter_by(kata_kunci=("HDNS-JR-RP"+kode_luas)).first()

        else :
            # harga dasar ukuran reklame (HDUR)
            HDUR = variabel_perhitungan.filter_by(kata_kunci=("HDUR-"+jenis_reklame.kata_kunci)).first()
            
            # harga dasar nilai strategis pemasangan reklame (HDNSPR)
            HDNSPR = variabel_perhitungan.filter_by(kata_kunci=("HDNS-"+jenis_reklame.kata_kunci)).first()

        #nilai luas reklame (NLR)
        NLR = args['luas'] * args['muka'] * HDUR.nilai * (1 + TTM)

        #nilai sudut pandang (NSP)
        FSP = variabel_perhitungan.filter_by(nama = args["sudut_pandang"]).first()
        NSP = FSP.nilai * HDNSPR.nilai

        #nilai fungsi ruang (NFR)
        FR = variabel_perhitungan.filter_by(nama = args["letak_pemasangan"]).first()
        NFR = FR.nilai * HDNSPR.nilai

        #nilai fungsi jalan (NFJ)
        FJ = variabel_perhitungan.filter_by(nama = args["klasifikasi_jalan"]).first()
        NFJ = FJ.nilai * HDNSPR.nilai

        #nilai strategis pemasangan reklame (NSPR)
        NSPR = NSP + NFR + NFJ

        #nilai jual objek pajak reklame (NJOPR)
        NJOPR = NLR + NKR

        #nilai sewa reklame (NSR)
        NSR = NSPR + NJOPR

        #total pajak
        tarif_pajak = variabel_perhitungan.filter_by(kata_kunci = "TPR").first()
        jumlah_termin = 1 
        if args["jangka_waktu_pajak"] == "Mingguan":
            selisih_hari = str(objek_pajak.tanggal_pembongkaran - objek_pajak.tanggal_pemasangan)
            selisih_hari = selisih_hari.split(" ")
            selisih_hari = int(selisih_hari[0])
            jumlah_termin = math.ceil(selisih_hari/7)
        elif args ["jangka_waktu_pajak"] == "Tahunan":
            selisih_hari = str(objek_pajak.tanggal_pembongkaran - objek_pajak.tanggal_pemasangan)
            selisih_hari = selisih_hari.split(" ")
            selisih_hari = int(selisih_hari[0])
            jumlah_termin = math.ceil(selisih_hari/365)
        
        total_pajak = args["jumlah"] * jumlah_termin *  tarif_pajak.nilai * NSR

        print(selisih_hari)
        # menambah data laporan baru
        nomor_skpd = str(5000 + objek_pajak.id)
        laporan = Laporan(
            objek_pajak.id, nomor_skpd, NFJ, NFR, NSP, HDNSPR.nilai, NKR, HDKR.nilai, NLR, HDUR.nilai, NJOPR,
            NSPR, NSR, tarif_pajak.nilai, total_pajak, jumlah_termin 
            )
        print(total_pajak)
        db.session.add(laporan)
        db.session.commit()

        return {"objek_pajak":marshal(objek_pajak, ObjekPajak.response_fields),
                "laporan": marshal(laporan, Laporan.response_fields),
                "selisih_hari": selisih_hari
                }, 200, {'Content-Type': 'application/json'}

    # fungsi untuk menghitung laporan pajak
    @jwt_required
    @payer_required
    def put(self):
        verify_jwt_in_request() 
        payer_claims_data = get_jwt_claims()
        payer = Payer.query.get(payer_claims_data["id"])
        parser = reqparse.RequestParser()
        parser.add_argument('nama_reklame', location='json', required=True)
        parser.add_argument('judul_reklame', location='json', required=True)
        parser.add_argument('tipe_reklame', location='json', required=True)
        parser.add_argument('jenis_reklame', location='json', required=True)
        parser.add_argument('foto', location='json', required=True)
        parser.add_argument('panjang', type=float, location='json', required=True)
        parser.add_argument('lebar', type=float, location='json', required=True)
        parser.add_argument('tinggi', type=float, location='json', required=True)
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
        parser.add_argument('jangka_waktu_pajak', location='json', required=True)

        args = parser.parse_args()

        get_id = ObjekPajak.query.order_by(desc('id')).first()
        if get_id is None:
            nopd = "1001"
        else :
            nopd = str(1000+get_id.id+1)
            
        variabel_perhitungan = VariabelPerhitungan.query
        #perhitungan total pajak yang harus dibayar oleh payer
        #tarif tambahan
        TTM = variabel_perhitungan.filter_by(nama = args["tarif_tambahan"]).first()
        TTM = TTM.nilai

        #nilai ketinggian reklame (NKR)
        jenis_reklame = variabel_perhitungan.filter_by(nama = args["jenis_reklame"]).first()
        HDKR = variabel_perhitungan.filter_by(kata_kunci = ("HDKR-"+jenis_reklame.kata_kunci)).first()
        NKR = args["tinggi"] * HDKR.nilai * (1 + TTM)

        if args["tipe_reklame"] == "Reklame Permanen" :    
            # harga dasar ukuran reklame (HDUR)
            if args["luas"] <= 10 :
                kode_luas = "-0"
            elif args["luas"] > 50 :
                kode_luas = "-50"
            else :
                kode_luas = "-10"
            HDUR = variabel_perhitungan.filter_by(kata_kunci=("HDUR-"+jenis_reklame.kata_kunci + kode_luas)).first()

            # harga dasar nilai strategis pemasangan reklame (HDNSPR)
            if args["luas"] < 3 :
                kode_luas = "-0"
            elif args["luas"] < 10 :
                kode_luas = "-3"
            elif args["luas"] <= 50 :
                kode_luas = "-10"
            else :
                kode_luas = "-50"
            HDNSPR = variabel_perhitungan.filter_by(kata_kunci=("HDNS-JR-RP"+kode_luas)).first()

        else :
            # harga dasar ukuran reklame (HDUR)
            HDUR = variabel_perhitungan.filter_by(kata_kunci=("HDUR-"+jenis_reklame.kata_kunci)).first()
            
            # harga dasar nilai strategis pemasangan reklame (HDNSPR)
            HDNSPR = variabel_perhitungan.filter_by(kata_kunci=("HDNS-"+jenis_reklame.kata_kunci)).first()

        #nilai luas reklame (NLR)
        NLR = args['luas'] * args['muka'] * HDUR.nilai * (1 + TTM)

        #nilai sudut pandang (NSP)
        FSP = variabel_perhitungan.filter_by(nama = args["sudut_pandang"]).first()
        NSP = FSP.nilai * HDNSPR.nilai

        #nilai fungsi ruang (NFR)
        FR = variabel_perhitungan.filter_by(nama = args["letak_pemasangan"]).first()
        NFR = FR.nilai * HDNSPR.nilai

        #nilai fungsi jalan (NFJ)
        FJ = variabel_perhitungan.filter_by(nama = args["klasifikasi_jalan"]).first()
        NFJ = FJ.nilai * HDNSPR.nilai

        #nilai strategis pemasangan reklame (NSPR)
        NSPR = NSP + NFR + NFJ

        #nilai jual objek pajak reklame (NJOPR)
        NJOPR = NLR + NKR

        #nilai sewa reklame (NSR)
        NSR = NSPR + NJOPR

        #total pajak
        tarif_pajak = variabel_perhitungan.filter_by(kata_kunci = "TPR").first()
        jumlah_termin = 1 
        if args["jangka_waktu_pajak"] == "Mingguan":
            selisih_hari = str(datetime.strptime(args["tanggal_pembongkaran"], "%Y-%m-%d") - datetime.strptime(args["tanggal_pemasangan"], "%Y-%m-%d"))
            selisih_hari = selisih_hari.split(" ")
            selisih_hari = int(selisih_hari[0])
            jumlah_termin = math.ceil(selisih_hari/7)
        elif args ["jangka_waktu_pajak"] == "Tahunan":
            selisih_hari = str(datetime.strptime(args["tanggal_pembongkaran"], "%Y-%m-%d") - datetime.strptime(args["tanggal_pemasangan"], "%Y-%m-%d"))
            selisih_hari = selisih_hari.split(" ")
            selisih_hari = int(selisih_hari[0])
            jumlah_termin = math.ceil(selisih_hari/365)
        
        total_pajak = args["jumlah"] * jumlah_termin *  tarif_pajak.nilai * NSR

        return {
            "laporan":{
                "nfj": NFJ,
                "nfr": NFR,
                "nsp": NSP,
                "hdnspr": HDNSPR.nilai,
                "nkr": NKR,
                "hdkr": HDKR.nilai,
                "nlr": NLR,
                "hdur": HDUR.nilai,
                "njopr": NJOPR,
                "nspr": NSPR,
                "nsr": NSR,
                "tarif_pajak": tarif_pajak.nilai,
                "total_pajak": total_pajak,
                "jumlah_termin": jumlah_termin,
            }
        }, 200, {'Content-Type': 'application/json'}

api.add_resource(ObjekPajakResource, '/payer')