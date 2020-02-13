import json, hashlib, logging
from . import user, create_token, reset_db
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, payer_required

class TestLaporan():

    # GET Semua Data Laporan milik Payer
    def test_laporan_get_all(self, user):
        reset_db()
        token = create_token(role='payer')
        data = {}
        res = user.get("/laporan/payer", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

    # GET Data Laporan milik Payer berdasarkan laporan id-nya (sukses)
    def test_laporan_get_id1(self, user):
        token = create_token(role='payer')
        data = {}
        res = user.get("/laporan/payer/1", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

    # GET Data Laporan milik Payer berdasarkan laporan id-nya (id laporan tidak ada)
    def test_laporan_get_id100(self, user):
        token = create_token(role='payer')
        data = {}
        res = user.get("/laporan/payer/100", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404

    # PUT Data Laporan milik Payer untuk membatalkan laporan (sukses)
    def test_laporan_put_batal(self, user):
        token = create_token(role='payer')
        data = {
            "laporan_id":2,
            "status_pembatalan":True
        }
        res = user.put("/laporan/payer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

    # PUT Data Laporan milik Payer untuk membatalkan laporan (id laporan tidak ada)
    def test_laporan_put_batal100(self, user):
        token = create_token(role='payer')
        data = {
            "laporan_id":100,
            "status_pembatalan":True
        }
        res = user.put("/laporan/payer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404

    # PUT Data Laporan milik Payer untuk mengubah status pembayaran (sukses)
    def test_laporan_put_bayar(self, user):
        token = create_token(role='payer')
        data = {
            "laporan_id":2,
            "status_pembayaran":True
        }
        res = user.put("/laporan/payer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
