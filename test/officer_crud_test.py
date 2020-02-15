import json, hashlib, logging
from . import user, create_token, reset_db
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, payer_required

class TestOfficer():

    # GET Data Officer
    def test_officer_get(self, user):
        reset_db()
        token = create_token(role='officer')
        data = {}
        res = user.get("/officers", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

    # GET Data Surveyor
    def test_surveyor_get(self, user):
        token = create_token(role='surveyor')
        data = {}
        res = user.get("/officers/surveyor", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

