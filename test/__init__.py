import pytest, logging, hashlib, json
from flask import Flask, request
from app import cache
from blueprints import app, db
from blueprints.payer.model import Payer
from blueprints.officer.model import Officer
from blueprints.daerah.model import Daerah
from blueprints.objek_pajak.model import ObjekPajak
from blueprints.laporan.model import Laporan
from blueprints.bukti_pembayaran.model import BuktiPembayaran
from blueprints.kode_qr.model import KodeQR
from blueprints.variabel_perhitungan.model import VariabelPerhitungan

def call_user(request):
    user = app.test_client()
    return user

def reset_db():
    db.drop_all()
    db.create_all()
    daerah = Daerah("Kabupaten Bandung Barat")
    db.session.add(daerah)
    db.session.commit()

    officer = Officer("P2001", "d54d1702ad0f8326224b817c796763c9", "officer1", "officer", 1)
    surveyor = Officer("P2002", "d54d1702ad0f8326224b817c796763c9", "surveyor1", "surveyor", 1)
    payer = Payer("P1002", "d54d1702ad0f8326224b817c796763c9", "payer1", 1, "Warung Pecel Ayam", "Jalan Galunggung")
    db.session.add(officer)
    db.session.add(surveyor)
    db.session.add(payer)
    db.session.commit()

    objek_pajak1 = ObjekPajak(1, '1001', 'Iklan Perumahan', 'Harga mulai dari 300 juta', 'Reklame Non Permanen', 'Spanduk, Umbul-umbul, Banner, Layar Toko','https://sribu-sg.s3.amazonaws.com/assets/media/contest_detail/2016/11/desain-banner-untuk-center-park-5839ad95faaa266f0000a583/normal_d432e6fb30.jpg',1, 2, 3, 3, '2020-01-15 14:29:36', '2020-01-25 14:29:36', 'Januari 2020', '112.609817', '-7.965917','Jalan Tidar, Malang', 1, 2,'Non Rokok/Miras', 'Kawasan Umum','Jalan Kabupaten','1 arah')
    objek_pajak2 = ObjekPajak(1, '1002', 'Iklan Konser', 'Konser Akbar Raisa', 'Reklame Permanen', 'Billboard/Bando','https://sribu-sg.s3.amazonaws.com/assets/media/contest_detail/2016/11/desain-banner-untuk-center-park-5839ad95faaa266f0000a583/normal_d432e6fb30.jpg',1, 2, 3, 2, '2020-01-15 14:29:36', '2020-01-25 14:29:36', 'Februari 2020', '112.6237303', '-7.97509837','Jalan Tenes, Malang', 1, 2,'Non Rokok/Miras', 'Kawasan Umum','Jalan Kabupaten','1 arah')
    db.session.add(objek_pajak1)
    db.session.add(objek_pajak2)
    db.session.commit()

    laporan1 = Laporan(1, '5001', 60000, 240000, 87500, 50000, 0, 0, 28000, 14000, 28000, 387500, 415500, 0.25, 207750, 1)
    laporan2 = Laporan(2, '5002', 60000, 240000, 87500, 50000, 0, 0, 28000, 14000, 28000, 387500, 415500, 0.25, 207750, 1)
    db.session.add(laporan1)
    db.session.add(laporan2)
    db.session.commit()

    bukti_pembayaran1 = BuktiPembayaran(1, 1, 9001, 3)
    bukti_pembayaran2 = BuktiPembayaran(2, 1, 9002, 2)
    db.session.add(bukti_pembayaran1)
    db.session.add(bukti_pembayaran2)
    bukti_pembayaran2.status_buat_kode_qr = True
    db.session.commit()


    kode_qr1 = KodeQR(1, 'alterratax123451', 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=alterratax123451')
    kode_qr2 = KodeQR(1, 'alterratax123452', 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=alterratax123452')
    kode_qr3 = KodeQR(1, 'alterratax123453', 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=alterratax123453')
    db.session.add(kode_qr1)
    db.session.add(kode_qr2)
    db.session.add(kode_qr3)
    db.session.commit()

    variabel1 = VariabelPerhitungan('Tarif Pajak Reklame', '', 'TPR', 0.25)
    variabel2 = VariabelPerhitungan('Non Rokok/Miras','TTM', 'TTNR', 0)
    variabel3 = VariabelPerhitungan('Rokok/Miras','TTM', 'TTR', 0.25)
    variabel4 = VariabelPerhitungan('Reklame Permanen','JR', 'JR-RP',0)
    variabel5 = VariabelPerhitungan('Billboard/Bando','JR-RP', 'JR-RP-B',0)
    variabel6 = VariabelPerhitungan('Reklame Non Permanen','JR', 'JR-RNP',0)
    variabel7 = VariabelPerhitungan('Spanduk, Umbul-umbul, Banner, Layar Toko','JR-RNP', 'JR-RNP-KS',0)
    variabel8 = VariabelPerhitungan('HDUR Billboard/Bando < 10m2','HDUR', 'HDUR-JR-RP-B-0', 525000)
    variabel9 = VariabelPerhitungan('HDUR Billboard/Bando 10-50m2','HDUR', 'HDUR-JR-RP-B-10', 800000)
    variabel10 = VariabelPerhitungan('HDUR Billboard/Bando > 50m2','HDUR', 'HDUR-JR-RP-B-50', 1200000)
    variabel11 = VariabelPerhitungan('HDUR Spanduk, Umbul-umbul, Banner, Layar Toko','HDUR', 'HDUR-JR-RNP-KS', 14000)
    variabel12 = VariabelPerhitungan('HDKR Billboard/Bando','HDKR', 'HDKR-JR-RP-B', 75000)
    variabel13 = VariabelPerhitungan('HDKR Spanduk, Umbul-umbul, Banner, Layar Toko','HDKR', 'HDKR-JR-RNP-KS', 0)
    variabel14 = VariabelPerhitungan('HDNS Reklame Permanen - Luas - 0-3m2','HDNSPR', 'HDNS-JR-RP-0', 220000)
    variabel15 = VariabelPerhitungan('HDNS Reklame Permanen - Luas - 3-3,99m2','HDNSPR', 'HDNS-JR-RP-3', 450000)
    variabel16 = VariabelPerhitungan('HDNS Reklame Permanen - Luas - 10-50m2','HDNSPR', 'HDNS-JR-RP-10', 527000)
    variabel17 = VariabelPerhitungan('HDNS Reklame Permanen - Luas - >50m2','HDNSPR', 'HDNS-JR-RP-50', 1000000)
    variabel18 = VariabelPerhitungan('HDNS Reklame Spanduk, Umbul-umbul, Banner, Layar Toko','HDNSPR', 'HDNS-JR-RNP-KS', 50000)
    variabel19 = VariabelPerhitungan('Kawasan Khusus','FR', 'FRKK', 6)
    variabel20 = VariabelPerhitungan('Kawasan Umum','FR', 'FRKU', 4.8)
    variabel21 = VariabelPerhitungan('Jalan Kabupaten','FJ', 'FJJK', 1.2)
    variabel22 = VariabelPerhitungan('1 arah','FSP', 'FSP1', 1.75)
    db.session.add(variabel1)
    db.session.add(variabel2)
    db.session.add(variabel3)
    db.session.add(variabel4)
    db.session.add(variabel5)
    db.session.add(variabel6)
    db.session.add(variabel7)
    db.session.add(variabel8)
    db.session.add(variabel9)
    db.session.add(variabel10)
    db.session.add(variabel11)
    db.session.add(variabel12)
    db.session.add(variabel13)
    db.session.add(variabel14)
    db.session.add(variabel15)
    db.session.add(variabel16)
    db.session.add(variabel17)
    db.session.add(variabel18)
    db.session.add(variabel19)
    db.session.add(variabel20)
    db.session.add(variabel21)
    db.session.add(variabel22)
    db.session.commit()

@pytest.fixture
def user(request):
    return call_user(request)

def create_token(role):
    if role == 'officer': 
        cache_user = "test_token_officer"
    elif role == 'surveyor' :
        cache_user = "test_token_surveyor"    
    else: 
        cache_user = "test_token_payer"
    token = cache.get(cache_user)
    if token is None:
        # prepare request input
        if role == 'officer':
            data = {
                "nip": "P2001",
                "pin": "11223344"
            }
        elif role == 'surveyor':
            data = {
                "nip": "P2002",
                "pin": "11223344"
            }
        else:
            data = {
                "npwpd": "P1002",
                "pin": "11223344"
            }
        # do request
        req = call_user(request)
        res = req.post("/login/", json=data)
        # store response
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        # compare with expected result
        assert res.status_code == 200
        assert res_json["message"] == "Token is successfully created"
        # save token into cache
        cache.set(cache_user, res_json["token"], timeout=30)
        # return
        return res_json["token"]
    return token