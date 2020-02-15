from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_claims
from datetime import timedelta
from functools import wraps
from flask_cors import CORS
import json, random, string, os

app = Flask(__name__) # membuat semua blueprint
app.config["APP_DEBUG"] = True
CORS(app)
# JWT Config
app.config["JWT_SECRET_KEY"] = "".join(random.choice(string.ascii_letters) for i in range(32))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)

# SQLAlchemy Config
try:
    env = os.environ.get('FLASK_ENV', 'development')
    if env == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Alterra@123@127.0.0.1:3306/rest_projek_reklame_test'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:seshasab072917@rest-portofolio.cmm0q8q3tp0t.ap-southeast-1.rds.amazonaws.com:3306/rest_projek_reklame'
except Exception as e:
    raise e

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#fungsi untuk authentifikasi user sebagai officer
def officer_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims["role"] != "officer":
            return {"status": "FORBIDDEN", "message": "You should be an officer to access this point"}, 403
        return fn(*args, **kwargs)
    return wrapper

#fungsi untuk authentifikasi user sebagai surveyor
def surveyor_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims["role"]!="surveyor":
            return {"status": "FORBIDDEN", "message": "You should be a surveyor to access this point"}, 403
        return fn(*args, **kwargs)
    return wrapper

#fungsi untuk authentifikasi user sebagai payer
def payer_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims["role"]!="payer":
            return {"status": "FORBIDDEN", "message": "You should be a payer to access this point"}, 403
        return fn(*args, **kwargs)
    return wrapper

#fungsi untuk record log
@app.after_request
def after_request(response):
    try:
        request_data = request.get_json()
    except:
        request_data = request.args.to_dict()
    if response.status_code == 200:
        app.logger.info("REQUEST_LOG\t%s", json.dumps({
            "method": request.method,
            "code": response.status,
            "request": request_data,
            "response": json.loads(response.data.decode("utf-8"))
        }))
    else:
        app.logger.error("REQUEST_LOG\t%s", json.dumps({
            "method": request.method,
            "code": response.status,
            "request": request_data,
            "response": json.loads(response.data.decode("utf-8"))
        }))
    return response

from blueprints.auth import blueprint_auth
from blueprints.daerah.model import blueprint_daerah
from blueprints.objek_pajak.resources import blueprint_objek_pajak
from blueprints.laporan.resources import blueprint_laporan
from blueprints.bukti_pembayaran.resources import blueprint_bukti_pembayaran
from blueprints.kode_qr.resources import blueprint_kode_qr
from blueprints.variabel_perhitungan.resources import blueprint_variabel_perhitungan
from blueprints.officer.resources import blueprint_officer
from blueprints.payer.resources import blueprint_payer

app.register_blueprint(blueprint_auth, url_prefix="/login")
app.register_blueprint(blueprint_officer, url_prefix="/officers")
app.register_blueprint(blueprint_payer, url_prefix="/payers")
app.register_blueprint(blueprint_kode_qr, url_prefix="/kode_qr")
app.register_blueprint(blueprint_bukti_pembayaran, url_prefix="/bukti_pembayaran")
app.register_blueprint(blueprint_objek_pajak, url_prefix="/objek_pajak")
app.register_blueprint(blueprint_variabel_perhitungan, url_prefix="/variabel_hitung")
app.register_blueprint(blueprint_laporan, url_prefix="/laporan")

db.create_all()
