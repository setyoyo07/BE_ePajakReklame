import json, hashlib, logging
from . import user, create_token, reset_db
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, payer_required, officer_required, payer_required

class TestKodeQR():

    # GET Data Kode QR berdasarkan id-nya oleh Officer (sukses)
    def test_kode_qr_get_id_officer(self, user):
        reset_db()
        token = create_token(role='officer')
        data = {}
        res = user.get("/kode_qr/officer/1", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

    # GET Data Kode QR berdasarkan id-nya oleh Officer (id tidak ditemukan)
    def test_kode_qr_get_id1000(self, user):
        reset_db()
        token = create_token(role='officer')
        data = {}
        res = user.get("/kode_qr/officer/1000", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404

    # POST Data Kode QR baru oleh Officer (sukses)
    def test_kode_qr_post_officer(self, user):
        token = create_token(role='officer')
        data = {
            "bukti_pembayaran_id":1
        }
        res = user.post("/kode_qr/officer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

    # POST Data Kode QR baru oleh Officer (kode qr sudah digenerate)
    def test_kode_qr_post_officer_done(self, user):
        token = create_token(role='officer')
        data = {
            "bukti_pembayaran_id":2
        }
        res = user.post("/kode_qr/officer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 400

    # POST Data Kode QR baru oleh Officer (bukti pembayaran id tidak ditemukan)
    def test_kode_qr_post_officer1000(self, user):
        token = create_token(role='officer')
        data = {
            "bukti_pembayaran_id":1000
        }
        res = user.post("/kode_qr/officer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404

    # GET Semua Data Kode QR dalam suatu objek_pajak oleh officer 
    def test_kode_qr_get_all(self, user):
        token = create_token(role='officer')
        data = {
            "bukti_pembayaran_id":1,
        }
        res = user.get("/kode_qr/officer", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

    # GET Data Kode QR dalam suatu objek_pajak oleh officer search berdasarkan id kode qr 
    def test_kode_qr_get_id(self, user):
        token = create_token(role='officer')
        data = {
            "bukti_pembayaran_id":1,
            "kode_QR_id":1
        }
        res = user.get("/kode_qr/officer", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

    # GET Semua Data Kode QR dalam suatu objek_pajak oleh payer
    def test_kode_qr_get_all_payer(self, user):
        token = create_token(role='payer')
        data = {
            "bukti_pembayaran_id":1,
        }
        res = user.get("/kode_qr/payer", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

    # GET Semua Data Kode QR dalam suatu objek_pajak oleh payer search berdasarkan id kode qr
    def test_kode_qr_get_id_payer(self, user):
        token = create_token(role='payer')
        data = {
            "bukti_pembayaran_id":1,
            "kode_QR_id":1
        }
        res = user.get("/kode_qr/payer", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

    # GET Data Kode QR berdasarkan id nya
    def test_kode_qr_get_byid(self, user):
        token = create_token(role='payer')
        data = {}
        res = user.get("/kode_qr/payer/1", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

    # GET Data Kode QR berdasarkan id nya (idtidak ditemukan)
    def test_kode_qr_get_byid1000(self, user):
        token = create_token(role='payer')
        data = {}
        res = user.get("/kode_qr/payer/1000", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404

    # POST Data Kode QR untuk generate kode qr oleh payer
    def test_kode_qr_post_payer(self, user):
        token = create_token(role='officer')
        data = {
            "nomor_sspd":"12345",
            "jumlah_reklame":1
        }
        res = user.post("/bukti_pembayaran/officer", json=data, headers={"Authorization": "Bearer "+token})
        
        token = create_token(role='payer')
        data = {
            "bukti_pembayaran_id":3
        }
        res = user.post("/kode_qr/payer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

    # POST Data Kode QR untuk generate kode qr oleh payer (id tidak ditemukan)
    def test_kode_qr_post_payer1000(self, user):
        token = create_token(role='payer')
        data = {
            "bukti_pembayaran_id":1000
        }
        res = user.post("/kode_qr/payer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404

    # POST Data Kode QR untuk generate kode qr oleh payer (kode qr sudah digenerate)
    def test_kode_qr_post_payer1(self, user):
        token = create_token(role='payer')
        data = {
            "bukti_pembayaran_id":1
        }
        res = user.post("/kode_qr/payer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 404

    # PUT Data Kode QR untuk merubah status scan oleh surveyor (sukses)
    def test_kode_qr_put_surveyor(self, user):
        token = create_token(role='surveyor')
        data = {
            "kode_unik":"alterratax123453"
        }
        res = user.put("/kode_qr/surveyor", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

    # PUT Data Kode QR untuk merubah status scan oleh surveyor (sudah discan)
    def test_kode_qr_put_surveyor_done(self, user):
        token = create_token(role='surveyor')
        data = {
            "kode_unik":"alterratax123451"
        }
        res = user.put("/kode_qr/surveyor", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

    # PUT Data Kode QR untuk merubah status scan oleh surveyor (invalid)
    def test_kode_qr_put_surveyor_invalid(self, user):
        token = create_token(role='surveyor')
        data = {
            "kode_unik":"alterratax"
        }
        res = user.put("/kode_qr/surveyor", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200