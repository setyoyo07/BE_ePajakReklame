import json, hashlib, logging
from . import user, create_token, reset_db
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, payer_required

class TestPayer():
    reset_db()

    # GET Data Payer
    def test_payer_get(self, user):
        token = create_token(role='payer')
        data = {}
        res = user.get("/payers", query_string=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
    
