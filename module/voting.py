from .blockchain import Blockchain, Block
from .session import UserManager
from .database import konekdb
import datetime
import hashlib


mydb, cur = konekdb()
blockchain = Blockchain()

user_manager = UserManager()
user_manager.buat_tabel()

def user_session():
    print(
        "Pilih opsi ini: \n",
        "1. Login\n",
        "2. Daftar"
        )
    pilihan = input("input: ")
    if pilihan == '1':
        print(">>>   Login Session   <<<")
        nis = input("Masukkan NIS: ")
        password = input("Masukkan Password: ")
        user = user_manager.login(nis, password)
        if user is not None:
            cek_pemilih(user[0])

    elif pilihan == '2':
        print(">>>   Signup Session   <<<")
        print("Masukkan data diri: ")
        nis = input("Masukkan NIS: ")
        nama = input("Ketik Namamu: ")
        kelas = input("Masukkan Kelas: ")
        password = input("Masukkan Password: ")
        user_manager.signup(nis, nama, password, kelas)
        user = user_manager.login(nis, password)
        if user is not None:
            cek_pemilih(user[0])

def list_kandidat():
    cur.execute("SELECT Nama FROM kandidat")
    kandidat = cur.fetchall()
    
    # Tampilkan kandidat kepada pengguna
    pilihan_dict = {}
    for index, siswa in enumerate(kandidat, start=1):
        pilihan_dict[str(index)] = siswa[0]  # Simpan pilihan indeks dan nama kandidat
    return pilihan_dict


def voting(nis,pilihan):
    pilihan_dict = list_kandidat() 
    # Validasi input pengguna
    if pilihan in pilihan_dict:
        nama_kandidat = pilihan_dict[pilihan]
        
        # Dapatkan NIS kandidat dari nama
        cur.execute("SELECT NIS FROM kandidat WHERE Nama = %s", (nama_kandidat,))
        nis_kandidat = cur.fetchone()
        
        if nis_kandidat:
            vote(str(nis), str(nis_kandidat[0])) # Panggil fungsi vote
        else:
            print("Kandidat tidak ditemukan.")
    else:
        print("Pilihan tidak valid atau GOLPUT.")

def vote(nis, nis_kandidat):
    cur.execute("SELECT Nama FROM kandidat WHERE NIS = %s", (nis_kandidat,))
    kandidat = cur.fetchone()
    new_vote = {
        'NIS Voter': hashlib.sha256(str(nis).encode()).hexdigest(),
        'Kandidat Terpilih': f"{kandidat[0]}",
        'Timestamp': datetime.datetime.now().isoformat()
    }

    # buat block baru
    vote_index = len(blockchain.chain)
    timestamp = datetime.datetime.now()
    data = new_vote
    previous_hash = blockchain.chain[-1].hash if blockchain.chain else "0"
    new_block = Block(vote_index, timestamp, data, previous_hash)

    # validasi block
    blockchain.validate_block(new_block)
    pemilih(nis,nis_kandidat)

def pemilih(nis,nis_kandidat):
    cur.execute("SELECT * FROM users WHERE NIS = %s", (nis,))
    user = cur.fetchone()
    if user:
        nama = user[1]
        cur.execute("INSERT INTO pemilih (NIS, nama, kandidat_yang_dipilih) VALUES (%s,%s,%s)", (nis,nama,nis_kandidat))
        mydb.commit()
        print("Terima kasih sudah memilih :)")
    else:
        print("NIS tidak ditemukan")

def cek_pemilih(nis):
    # Hanya panggil pembuatan tabel jika belum ada
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pemilih (
                NIS INT PRIMARY KEY,
                nama VARCHAR(255),
                kandidat_yang_dipilih INT
    )
    """)
    cur.execute("SELECT * FROM pemilih WHERE NIS = %s", (nis,))
    user = cur.fetchone()
    
    # Handle kasus ketika tidak ada pemilih yang ditemukan
    if user is None:
        return None
    else:
        return user

    # if user:
    #     error = True
    #     return error
    # else:
    #     voting(nis)
    
