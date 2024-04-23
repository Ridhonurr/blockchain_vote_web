from blockchain import Blockchain, Block
from session import UserManager
from database import konekdb
import datetime
import hashlib
import json

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
            voting(user[0])

    elif pilihan == '2':
        print(">>>   Signup Session   <<<")
        print("Masukkan data diri: ")
        nis = input("Masukkan NIS: ")
        nama = input("Ketik Namamu: ")
        kelas = input("Masukkan Kelas: ")
        password = input("Masukkan Password: ")
        user_manager.signup(nis, nama, password, kelas)
        user = user_manager.login(nis, password)
        user = user_manager.login(nis, password)
        if user is not None:
            voting(user[0])


def voting(nis):
    print("Pilih Kandidat yang Kamu Pilih: ")
    # Ambil kandidat dari database
    cur.execute("SELECT Nama FROM kandidat")
    kandidat = cur.fetchall()
    
    # Tampilkan kandidat kepada pengguna
    pilihan_dict = {}
    for index, siswa in enumerate(kandidat, start=1):
        pilihan_dict[str(index)] = siswa[0]  # Simpan pilihan indeks dan nama kandidat
        print(f"{index}. {siswa[0]}")
    
    # Dapatkan pilihan pengguna
    pilihankamu = input("Siapa yang kamu Pilih? (masukkan angka): ")

    # Validasi input pengguna
    if pilihankamu in pilihan_dict:
        nama_kandidat = pilihan_dict[pilihankamu]
        
        # Dapatkan NIS kandidat dari nama
        cur.execute("SELECT NIS FROM kandidat WHERE Nama = %s", (nama_kandidat,))
        nis_kandidat = cur.fetchone()
        
        if nis_kandidat:
            vote(str(nis), str(nis_kandidat[0]))  # Panggil fungsi vote
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


def main():
    print("\n",
        "|----------------------------------------------|\n",
        "|  Selamat Datang di Blockchain Voting System  |\n",
        "|----------------------------------------------|"
        )
    user_session()
    
    
if __name__ == '__main__':
    main()

