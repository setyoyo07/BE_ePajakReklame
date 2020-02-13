# import json, hashlib, logging
# from . import user, create_token, reset_db
# from flask_jwt_extended import jwt_required, get_jwt_claims
# from blueprints import db, payer_required, officer_required, payer_required

# class TestKodeQR():

#     # GET Data Kode QR berdasarkan id-nya oleh Officer
#     def test_bukti_pembayaran_get_all(self, user):
#         reset_db()
#         token = create_token(role='officer')
#         data = {}
#         res = user.get("/bukti_pembayaran/officer", query_string=data, headers={"Authorization": "Bearer "+token})
#         res_json = json.loads(res.data)
#         logging.warning("RESULT: %s", res_json)
#         assert res.status_code == 200

#     # # GET Data BUkti Pembayaran oleh Officer search by nomor sspd
#     # def test_bukti_pembayaran_get_search(self, user):
#     #     token = create_token(role='officer')
#     #     data = {
#     #         "nomor_sspd":"1000000"
#     #     }
#     #     res = user.get("/bukti_pembayaran/officer", query_string=data, headers={"Authorization": "Bearer "+token})
#     #     res_json = json.loads(res.data)
#     #     logging.warning("RESULT: %s", res_json)
#     #     assert res.status_code == 200

#     # # POST Data Bukti Pembayaran baru oleh Officer (sukses)
#     # def test_bukti_pembayaran_post(self, user):
#     #     token = create_token(role='officer')
#     #     data = {
#     #         "nomor_sspd":"12345",
#     #         "jumlah_reklame":1
#     #     }
#     #     res = user.post("/bukti_pembayaran/officer", json=data, headers={"Authorization": "Bearer "+token})
#     #     res_json = json.loads(res.data)
#     #     logging.warning("RESULT: %s", res_json)
#     #     assert res.status_code == 200

#     # # POST Data Bukti Pembayaran baru oleh Officer (jumlah kurang dari 1)
#     # def test_bukti_pembayaran_post0(self, user):
#     #     token = create_token(role='officer')
#     #     data = {
#     #         "nomor_sspd":"12345",
#     #         "jumlah_reklame":0
#     #     }
#     #     res = user.post("/bukti_pembayaran/officer", json=data, headers={"Authorization": "Bearer "+token})
#     #     res_json = json.loads(res.data)
#     #     logging.warning("RESULT: %s", res_json)
#     #     assert res.status_code == 400

#     # # POST Data Bukti Pembayaran baru oleh Officer (nomor sspd sudah ada)
#     # def test_bukti_pembayaran_post_sama(self, user):
#     #     token = create_token(role='officer')
#     #     data = {
#     #         "nomor_sspd":"9001",
#     #         "jumlah_reklame":1
#     #     }
#     #     res = user.post("/bukti_pembayaran/officer", json=data, headers={"Authorization": "Bearer "+token})
#     #     res_json = json.loads(res.data)
#     #     logging.warning("RESULT: %s", res_json)
#     #     assert res.status_code == 400

#     # # GET Data Bukti Pembayaran oleh Payer (sukses)
#     # def test_bukti_pembayaran_get_payer(self, user):
#     #     token = create_token(role='payer')
#     #     data = {}
#     #     res = user.get("/bukti_pembayaran/payer/1", query_string=data, headers={"Authorization": "Bearer "+token})
#     #     res_json = json.loads(res.data)
#     #     logging.warning("RESULT: %s", res_json)
#     #     assert res.status_code == 200

#     # # GET Data Bukti Pembayaran oleh Payer (laporan id tidak ditemukan)
#     # def test_bukti_pembayaran_get_payer1000(self, user):
#     #     token = create_token(role='payer')
#     #     data = {}
#     #     res = user.get("/bukti_pembayaran/payer/1000", query_string=data, headers={"Authorization": "Bearer "+token})
#     #     res_json = json.loads(res.data)
#     #     logging.warning("RESULT: %s", res_json)
#     #     assert res.status_code == 404

#     # # GET Semua Data Bukti Pembayaran oleh Surveyor
#     # def test_bukti_pembayaran_get_surveyor(self, user):
#     #     token = create_token(role='surveyor')
#     #     data = {}
#     #     res = user.get("/bukti_pembayaran/surveyor", query_string=data, headers={"Authorization": "Bearer "+token})
#     #     res_json = json.loads(res.data)
#     #     logging.warning("RESULT: %s", res_json)
#     #     assert res.status_code == 200

#     # # GET Data Bukti Pembayaran oleh Surveyor berdasarkan pembayaran id-nya
#     # def test_bukti_pembayaran_get_byid_surveyor(self, user):
#     #     token = create_token(role='surveyor')
#     #     data = {}
#     #     res = user.get("/bukti_pembayaran/surveyor/1", query_string=data, headers={"Authorization": "Bearer "+token})
#     #     res_json = json.loads(res.data)
#     #     logging.warning("RESULT: %s", res_json)
#     #     assert res.status_code == 200

#     # # PUT Data Bukti Pembayaran untuk menambah data bukti pelanggaran (sukses)
#     # def test_bukti_pembayaran_put_pelanggaran(self, user):
#     #     token = create_token(role='surveyor')
#     #     data = {
#     #         "bukti_pembayaran_id": 1,
#     #         "pelanggaran": "reklame berlebih"
#     #     }
#     #     res = user.put("/bukti_pembayaran/surveyor", json=data, headers={"Authorization": "Bearer "+token})
#     #     res_json = json.loads(res.data)
#     #     logging.warning("RESULT: %s", res_json)
#     #     assert res.status_code == 200
