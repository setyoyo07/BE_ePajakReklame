import json, hashlib, logging
from . import user, create_token, reset_db
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, payer_required

class TestVariabelPerhitungan():

    # GET Data Variabel Perhitungan
    def test_variabel_perhitungan_get(self, user):
        reset_db()
        token = create_token(role='payer')
        data = {}
        res = user.get("/variabel_hitung/payer", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200


