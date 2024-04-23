from database import konekdb
import hashlib

mydb, cur = konekdb()

class UserManager:
    def buat_tabel(self):
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
                    NIS INT PRIMARY KEY,
                    nama VARCHAR(255),
                    password VARCHAR(64),
                    kelas VARCHAR(10)
        )
        """)
    def login(self, nis, password):
        self.nis = nis
        self.password = hashlib.sha256(password.encode()).hexdigest()
        cur.execute("SELECT * FROM users WHERE NIS = %s AND password = %s", (self.nis, self.password))
        user = cur.fetchone()
        if user:
            print(f"Login Berhasil, Selamat Datang {user[1]}")
            return user
        else:
            print("NIS atau password salah!")
            return None
        
    def signup(self, nis, nama, password, kelas):
        self.nis = nis
        self.nama = nama
        self.kelas = kelas
        self.password = hashlib.sha256(password.encode()).hexdigest()
        cur.execute("INSERT INTO users (NIS,nama,password,kelas) VALUES (%s,%s,%s,%s)", (self.nis,self.nama,self.password,self.kelas))
        mydb.commit()
        print("Data siswa telah ditambahkan")

    def buat_kandidat(self,nis):
        self.nis = nis
        cur.execute("SELECT * FROM users WHERE NIS = %s", (self.nis,))
        user = cur.fetchone()
        if user:
            for row in user:
                cur.execute("INSERT INTO kandidat (NIS, Nama) VALUES (%s,%s)", (row[0],row[1]))
                mydb.commit()
                print(f"Selamat, {row[1]} terpilih menjadi kandidat")
        else:
            print("tidak ada siswa yang menggunakan NIS ini")
        