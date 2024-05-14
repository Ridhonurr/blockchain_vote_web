from .blockchain import Blockchain, Block
from .session import UserManager
from .database import konekdb
import datetime
import hashlib
from flask import g

def get_db():
    if 'db' not in g:
        g.db, g.cur = konekdb()
    return g.db, g.cur

user_manager = UserManager()
user_manager.buat_tabel()

def list_kandidat():
    db, cur = get_db()
    cur.execute("SELECT Nama FROM kandidat")
    kandidat = cur.fetchall()
    pilihan_dict = {}
    for index, siswa in enumerate(kandidat, start=1):
        pilihan_dict[str(index)] = siswa[0]
    return pilihan_dict

def voting(nis, pilihan):
    db, cur = get_db()
    pilihan_dict = list_kandidat()
    if pilihan in pilihan_dict:
        nama_kandidat = pilihan_dict[pilihan]
        cur.execute("SELECT NIS FROM kandidat WHERE Nama = %s", (nama_kandidat,))
        nis_kandidat = cur.fetchone()
        if nis_kandidat:
            vote(nis, nis_kandidat[0])
        else:
            print("Kandidat tidak ditemukan.")
    else:
        print("Pilihan tidak valid atau GOLPUT.")

def vote(nis, nis_kandidat):
    db, cur = get_db()
    blockchain = Blockchain()
    cur.execute("SELECT Nama FROM kandidat WHERE NIS = %s", (nis_kandidat,))
    kandidat = cur.fetchone()
    new_vote = {
        'NIS Voter': hashlib.sha256(str(nis).encode()).hexdigest(),
        'Kandidat Terpilih': f"{kandidat[0]}",
        'Timestamp': datetime.datetime.now().isoformat()
    }
    vote_index = len(blockchain.chain)
    timestamp = datetime.datetime.now()
    data = new_vote
    previous_hash = blockchain.chain[-1].hash if blockchain.chain else "0"
    new_block = Block(vote_index, timestamp, data, previous_hash)
    blockchain.validate_block(new_block)
    pemilih(nis, nis_kandidat)

def pemilih(nis, nis_kandidat):
    db, cur = get_db()
    cur.execute("SELECT * FROM users WHERE NIS = %s", (nis,))
    user = cur.fetchone()
    if user:
        nama = user[1]
        cur.execute("INSERT INTO pemilih (NIS, nama, kandidat_yang_dipilih) VALUES (%s, %s, %s)", (nis, nama, nis_kandidat))
        db.commit()
        print("Terima kasih sudah memilih :)")
    else:
        print("NIS tidak ditemukan")

def cek_pemilih(nis):
    db, cur = get_db()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pemilih (
        NIS INT PRIMARY KEY,
        nama VARCHAR(255),
        kandidat_yang_dipilih INT
    )
    """)
    cur.execute("SELECT * FROM pemilih WHERE NIS = %s", (nis,))
    user = cur.fetchone()
    return user
