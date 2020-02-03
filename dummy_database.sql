use rest_projek_reklame;
insert into daerah(nama)
	values('Kota Banda Aceh'),('Kota Medan'),('Kota Padang'),
    ('Kota Pekan Baru'),('Kota Jambi'),('Kota Palembang'),
    ('Kota Bengkulu'),('Kota Bandar Lampung'),('Kota Pangkalpinang'),
    ('Kota Tanjung Pinang'),('Kota Jakarta'),('Kota Bandung'),
    ('Kota Semarang'),('Kota Yogyakarta'),('Kota Surabaya'),
    ('Kota Serang'),('Kota Denpasar'),('Kota Mataram'),
    ('Kota Kupang'),('Kota Pontianak'),('Kota Palangka Raya'),
    ('Kota Banjarmasin'), ('Kota Samarinda'),('Kota Tanjung Selor'),
    ('Kota Manado'),('Kota Palu'),('Kota Makassar'),
    ('Kota Kendari'),('Kota Gorontalo'),('Kota Mamuju'),
    ('Kota Ambon'),('Kota Sofifi'),('Kota Jayapura'),
    ('Manokwari');
    
insert into variabel_perhitungan(tarif, tipe, biaya)
	values('Klasifikasi Jalan', 'Protokol A', 125000),
    ('Klasifikasi Jalan', 'Protokol B', 120000),
    ('Klasifikasi Jalan', 'Protokol C', 75000),
    ('Letak Pemasangan', 'Indoor', 50),
    ('Letak Pemasangan', 'Outdoor', 25),
    ('Tinggi Dari Tanah', 'Protokol A', 25000),
    ('Tinggi Dari Tanah', 'Protokol B', 24000),
    ('Tinggi Dari Tanah', 'Protokol C', 15000),
    ('Jenis Reklame', 'Billboard / Baliho Papan Listrik', 300000),
    ('Jenis Reklame', 'Billboard / Baliho Papan Nonlistrik', 250000),
    ('Jenis Reklame', 'Billboard / Baliho Besi Listrik', 500000),
    ('Jenis Reklame', 'Billboard / Baliho Besi Nonistrik', 400000),
    ('Jenis Reklame', 'Spanduk Plastik / Karet', 50000),
    ('Jenis Reklame', 'Umbul-umbul Plastik', 35000);
    
insert into payer(npwpd, pin, nama, daerah_id)
	values('P100000001122001', 'd54d1702ad0f8326224b817c796763c9', 'Payer1', 1),
    ('P100000001122002', 'd54d1702ad0f8326224b817c796763c9', 'Payer2', 1),
    ('P100000001122003', 'd54d1702ad0f8326224b817c796763c9', 'Payer3', 1);
    
insert into officer(nip, pin, nama, role, daerah_id)
	values('P200000001122001', 'd54d1702ad0f8326224b817c796763c9', 'Officer1', 'officer', 1),
    ('P200000001122002', 'd54d1702ad0f8326224b817c796763c9', 'Officer2', 'officer', 1),
    ('P200000001122003', 'd54d1702ad0f8326224b817c796763c9', 'Surveyor3', 'surveyor', 1);
    
insert into objek_pajak(payer_id, nopd, nama_reklame, judul_reklame, tipe_reklame, jenis_reklame,
                foto, panjang, lebar, tinggi, jumlah, tanggal_pemasangan, tanggal_pembongkaran, masa_pajak,
                longitude, latitude, lokasi, created_at, updated_at)
	values(1, '1010205051101', 'Iklan Perumahan', 'Harga mulai dari 300 juta', 'Insidentil', 'Spanduk',
			'https://sribu-sg.s3.amazonaws.com/assets/media/contest_detail/2016/11/desain-banner-untuk-center-park-5839ad95faaa266f0000a583/normal_d432e6fb30.jpg',
            1, 2, 3, 10, '2020-01-15 14:29:36', '2020-01-25 14:29:36', 1, '-7.965917', '112.609817', 'jalan tidar malang', now(), now());
            
insert into laporan(objek_pajak_id, tarif_klasifikasi_jalan, tarif_letak_pemasangan, tarif_njopr,
				tarif_tinggi_tanah, total_pajak, nomor_skpd, status_pembayaran, pembatalan_laporan,
                status_verifikasi, created_at, updated_at)
	values(1, 125000, 25, 100000, 0, 725000, '011511200801010001', True, False, True, now(), now());
    
insert into bukti_pembayaran(laporan_id, daerah_id, nomor_sspd, status_buat_kode_qr,
				pelanggaran, jumlah_reklame, created_at, updated_at)
	values(1, 1, 45524, True, '', 10, now(), now());
    
insert into kode_QR(bukti_pembayaran_id, kode_unik, link_gambar, status_scan,
				created_at, updated_at)
	values(1, '455240kodeunik', 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=455240kodeunik',
				True, now(), now()),
                (1, '455241kodeunik', 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=455241kodeunik',
				True, now(), now()),
				(1, '455242kodeunik', 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=455242kodeunik',
				True, now(), now()),
                (1, '455243kodeunik', 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=455243kodeunik',
				True, now(), now()),
                (1, '455244kodeunik', 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=455244kodeunik',
				True, now(), now()),
                (1, '455245kodeunik', 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=455245kodeunik',
				False, now(), now()),
                (1, '455246kodeunik', 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=455246kodeunik',
				False, now(), now()),
                (1, '455247kodeunik', 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=455247kodeunik',
				False, now(), now()),
                (1, '455248kodeunik', 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=455248kodeunik',
				False, now(), now()),
                (1, '455249kodeunik', 'https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=455249kodeunik',
				False, now(), now());
                
                
-- tespostkodeqr
insert into bukti_pembayaran(laporan_id, daerah_id, nomor_sspd, status_buat_kode_qr,
				pelanggaran, jumlah_reklame, created_at, updated_at)
	values(1, 1, 45525, True, '', 5, now(), now()); 