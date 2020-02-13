import json, hashlib, logging
from . import user, create_token, reset_db
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints import db, payer_required

class TestObjekPajak():

    # Post Objek Pajak Non Permanen
    def test_objek_pajak_post(self, user):
        reset_db()
        token = create_token(role='payer')
        data = {
            "nama_reklame":"iklan rumah makan",
            "judul_reklame":"buka tiap hari kecuali hari kiamat",
            "tipe_reklame":"Reklame Non Permanen",
            "jenis_reklame":"Spanduk, Umbul-umbul, Banner, Layar Toko",
            "foto":"https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTs8x_lK14Ik0KiZkPicpn7L0ZiMbk89HKsbdUmw3jCJvm9IvBt",
            "panjang":2,
            "lebar":1,
            "tinggi":3,
            "jumlah":2,
            "muka":1,
            "luas":2,
            "tanggal_pemasangan":"2020-02-10",
            "tanggal_pembongkaran":"2020-03-10",
            "masa_pajak":"Februari 2020",
            "lokasi":"Jalan Raya Tidar, Malang",
            "longitude":"112.609817",
            "latitude":"-7.965917",
            "tarif_tambahan":"Rokok/Miras",
            "letak_pemasangan":"Kawasan Umum",
            "klasifikasi_jalan":"Jalan Kabupaten",
            "sudut_pandang":"1 arah",
            "jangka_waktu_pajak":"Mingguan"
        }
        res = user.post("/objek_pajak/payer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

# Post Objek Pajak Permanen Luas <3 m2
    def test_objek_pajak_post2(self, user):
        token = create_token(role='payer')
        data = {
            "nama_reklame":"iklan rumah makan",
            "judul_reklame":"buka tiap hari kecuali hari kiamat",
            "tipe_reklame":"Reklame Permanen",
            "jenis_reklame":"Billboard/Bando",
            "foto":"https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTs8x_lK14Ik0KiZkPicpn7L0ZiMbk89HKsbdUmw3jCJvm9IvBt",
            "panjang":2,
            "lebar":1,
            "tinggi":3,
            "jumlah":2,
            "muka":1,
            "luas":2,
            "tanggal_pemasangan":"2020-02-10",
            "tanggal_pembongkaran":"2020-03-10",
            "masa_pajak":"Februari 2020",
            "lokasi":"Jalan Raya Tidar, Malang",
            "longitude":"112.609817",
            "latitude":"-7.965917",
            "tarif_tambahan":"Rokok/Miras",
            "letak_pemasangan":"Kawasan Umum",
            "klasifikasi_jalan":"Jalan Kabupaten",
            "sudut_pandang":"1 arah",
            "jangka_waktu_pajak":"Mingguan"
        }
        res = user.post("/objek_pajak/payer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

# Post Objek Pajak Permanen Luas <10 m2
    def test_objek_pajak_post3(self, user):
        token = create_token(role='payer')
        data = {
            "nama_reklame":"iklan rumah makan",
            "judul_reklame":"buka tiap hari kecuali hari kiamat",
            "tipe_reklame":"Reklame Permanen",
            "jenis_reklame":"Billboard/Bando",
            "foto":"https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTs8x_lK14Ik0KiZkPicpn7L0ZiMbk89HKsbdUmw3jCJvm9IvBt",
            "panjang":4,
            "lebar":2,
            "tinggi":3,
            "jumlah":2,
            "muka":1,
            "luas":8,
            "tanggal_pemasangan":"2020-02-10",
            "tanggal_pembongkaran":"2020-03-10",
            "masa_pajak":"Februari 2020",
            "lokasi":"Jalan Raya Tidar, Malang",
            "longitude":"112.609817",
            "latitude":"-7.965917",
            "tarif_tambahan":"Rokok/Miras",
            "letak_pemasangan":"Kawasan Umum",
            "klasifikasi_jalan":"Jalan Kabupaten",
            "sudut_pandang":"1 arah",
            "jangka_waktu_pajak":"Mingguan"
        }
        res = user.post("/objek_pajak/payer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

# Post Objek Pajak Permanen Luas <50 m2
    def test_objek_pajak_post4(self, user):
        token = create_token(role='payer')
        data = {
            "nama_reklame":"iklan rumah makan",
            "judul_reklame":"buka tiap hari kecuali hari kiamat",
            "tipe_reklame":"Reklame Permanen",
            "jenis_reklame":"Billboard/Bando",
            "foto":"https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTs8x_lK14Ik0KiZkPicpn7L0ZiMbk89HKsbdUmw3jCJvm9IvBt",
            "panjang":10,
            "lebar":2,
            "tinggi":3,
            "jumlah":2,
            "muka":1,
            "luas":20,
            "tanggal_pemasangan":"2020-02-10",
            "tanggal_pembongkaran":"2020-03-10",
            "masa_pajak":"Februari 2020",
            "lokasi":"Jalan Raya Tidar, Malang",
            "longitude":"112.609817",
            "latitude":"-7.965917",
            "tarif_tambahan":"Rokok/Miras",
            "letak_pemasangan":"Kawasan Umum",
            "klasifikasi_jalan":"Jalan Kabupaten",
            "sudut_pandang":"1 arah",
            "jangka_waktu_pajak":"Mingguan"
        }
        res = user.post("/objek_pajak/payer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

# Post Objek Pajak Permanen Luas >50 m2
    def test_objek_pajak_post5(self, user):
        token = create_token(role='payer')
        data = {
            "nama_reklame":"iklan rumah makan",
            "judul_reklame":"buka tiap hari kecuali hari kiamat",
            "tipe_reklame":"Reklame Permanen",
            "jenis_reklame":"Billboard/Bando",
            "foto":"https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTs8x_lK14Ik0KiZkPicpn7L0ZiMbk89HKsbdUmw3jCJvm9IvBt",
            "panjang":20,
            "lebar":3,
            "tinggi":3,
            "jumlah":2,
            "muka":1,
            "luas":60,
            "tanggal_pemasangan":"2020-02-10",
            "tanggal_pembongkaran":"2020-03-10",
            "masa_pajak":"Februari 2020",
            "lokasi":"Jalan Raya Tidar, Malang",
            "longitude":"112.609817",
            "latitude":"-7.965917",
            "tarif_tambahan":"Rokok/Miras",
            "letak_pemasangan":"Kawasan Umum",
            "klasifikasi_jalan":"Jalan Kabupaten",
            "sudut_pandang":"1 arah",
            "jangka_waktu_pajak":"Tahunan"
        }
        res = user.post("/objek_pajak/payer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

# Put Objek Pajak Non Permanen
    def test_objek_pajak_put(self, user):
        reset_db()
        token = create_token(role='payer')
        data = {
            "nama_reklame":"iklan rumah makan",
            "judul_reklame":"buka tiap hari kecuali hari kiamat",
            "tipe_reklame":"Reklame Non Permanen",
            "jenis_reklame":"Spanduk, Umbul-umbul, Banner, Layar Toko",
            "foto":"https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTs8x_lK14Ik0KiZkPicpn7L0ZiMbk89HKsbdUmw3jCJvm9IvBt",
            "panjang":2,
            "lebar":1,
            "tinggi":3,
            "jumlah":2,
            "muka":1,
            "luas":2,
            "tanggal_pemasangan":"2020-02-10",
            "tanggal_pembongkaran":"2020-03-10",
            "masa_pajak":"Februari 2020",
            "lokasi":"Jalan Raya Tidar, Malang",
            "longitude":"112.609817",
            "latitude":"-7.965917",
            "tarif_tambahan":"Rokok/Miras",
            "letak_pemasangan":"Kawasan Umum",
            "klasifikasi_jalan":"Jalan Kabupaten",
            "sudut_pandang":"1 arah",
            "jangka_waktu_pajak":"Mingguan"
        }
        res = user.put("/objek_pajak/payer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

# Put Objek Pajak Permanen Luas <3 m2
    def test_objek_pajak_put2(self, user):
        token = create_token(role='payer')
        data = {
            "nama_reklame":"iklan rumah makan",
            "judul_reklame":"buka tiap hari kecuali hari kiamat",
            "tipe_reklame":"Reklame Permanen",
            "jenis_reklame":"Billboard/Bando",
            "foto":"https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTs8x_lK14Ik0KiZkPicpn7L0ZiMbk89HKsbdUmw3jCJvm9IvBt",
            "panjang":2,
            "lebar":1,
            "tinggi":3,
            "jumlah":2,
            "muka":1,
            "luas":2,
            "tanggal_pemasangan":"2020-02-10",
            "tanggal_pembongkaran":"2020-03-10",
            "masa_pajak":"Februari 2020",
            "lokasi":"Jalan Raya Tidar, Malang",
            "longitude":"112.609817",
            "latitude":"-7.965917",
            "tarif_tambahan":"Rokok/Miras",
            "letak_pemasangan":"Kawasan Umum",
            "klasifikasi_jalan":"Jalan Kabupaten",
            "sudut_pandang":"1 arah",
            "jangka_waktu_pajak":"Mingguan"
        }
        res = user.put("/objek_pajak/payer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

# Put Objek Pajak Permanen Luas <10 m2
    def test_objek_pajak_put3(self, user):
        token = create_token(role='payer')
        data = {
            "nama_reklame":"iklan rumah makan",
            "judul_reklame":"buka tiap hari kecuali hari kiamat",
            "tipe_reklame":"Reklame Permanen",
            "jenis_reklame":"Billboard/Bando",
            "foto":"https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTs8x_lK14Ik0KiZkPicpn7L0ZiMbk89HKsbdUmw3jCJvm9IvBt",
            "panjang":4,
            "lebar":2,
            "tinggi":3,
            "jumlah":2,
            "muka":1,
            "luas":8,
            "tanggal_pemasangan":"2020-02-10",
            "tanggal_pembongkaran":"2020-03-10",
            "masa_pajak":"Februari 2020",
            "lokasi":"Jalan Raya Tidar, Malang",
            "longitude":"112.609817",
            "latitude":"-7.965917",
            "tarif_tambahan":"Rokok/Miras",
            "letak_pemasangan":"Kawasan Umum",
            "klasifikasi_jalan":"Jalan Kabupaten",
            "sudut_pandang":"1 arah",
            "jangka_waktu_pajak":"Mingguan"
        }
        res = user.put("/objek_pajak/payer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

# Put Objek Pajak Permanen Luas <50 m2
    def test_objek_pajak_put4(self, user):
        token = create_token(role='payer')
        data = {
            "nama_reklame":"iklan rumah makan",
            "judul_reklame":"buka tiap hari kecuali hari kiamat",
            "tipe_reklame":"Reklame Permanen",
            "jenis_reklame":"Billboard/Bando",
            "foto":"https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTs8x_lK14Ik0KiZkPicpn7L0ZiMbk89HKsbdUmw3jCJvm9IvBt",
            "panjang":10,
            "lebar":2,
            "tinggi":3,
            "jumlah":2,
            "muka":1,
            "luas":20,
            "tanggal_pemasangan":"2020-02-10",
            "tanggal_pembongkaran":"2020-03-10",
            "masa_pajak":"Februari 2020",
            "lokasi":"Jalan Raya Tidar, Malang",
            "longitude":"112.609817",
            "latitude":"-7.965917",
            "tarif_tambahan":"Rokok/Miras",
            "letak_pemasangan":"Kawasan Umum",
            "klasifikasi_jalan":"Jalan Kabupaten",
            "sudut_pandang":"1 arah",
            "jangka_waktu_pajak":"Mingguan"
        }
        res = user.put("/objek_pajak/payer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200

# Put Objek Pajak Permanen Luas >50 m2
    def test_objek_pajak_put5(self, user):
        token = create_token(role='payer')
        data = {
            "nama_reklame":"iklan rumah makan",
            "judul_reklame":"buka tiap hari kecuali hari kiamat",
            "tipe_reklame":"Reklame Permanen",
            "jenis_reklame":"Billboard/Bando",
            "foto":"https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTs8x_lK14Ik0KiZkPicpn7L0ZiMbk89HKsbdUmw3jCJvm9IvBt",
            "panjang":20,
            "lebar":3,
            "tinggi":3,
            "jumlah":2,
            "muka":1,
            "luas":60,
            "tanggal_pemasangan":"2020-02-10",
            "tanggal_pembongkaran":"2020-03-10",
            "masa_pajak":"Februari 2020",
            "lokasi":"Jalan Raya Tidar, Malang",
            "longitude":"112.609817",
            "latitude":"-7.965917",
            "tarif_tambahan":"Rokok/Miras",
            "letak_pemasangan":"Kawasan Umum",
            "klasifikasi_jalan":"Jalan Kabupaten",
            "sudut_pandang":"1 arah",
            "jangka_waktu_pajak":"Tahunan"
        }
        res = user.put("/objek_pajak/payer", json=data, headers={"Authorization": "Bearer "+token})
        res_json = json.loads(res.data)
        logging.warning("RESULT: %s", res_json)
        assert res.status_code == 200
