import hashlib
import json
from database import konekdb
import datetime

mydb, cur = konekdb()  # Membuat koneksi ke database

# Buat tabel blockchain
cur.execute("""
CREATE TABLE IF NOT EXISTS blocks (
    vote_index INT PRIMARY KEY,
    timestamp TEXT,
    data TEXT,
    previous_hash VARCHAR(64),
    hash VARCHAR(64)
)
""")


class Block:
    def __init__(self, vote_index, timestamp, data, previous_hash):
        # Konversi vote_index ke int jika perlu
        self.vote_index = str(vote_index)
        # Konversi timestamp ke str jika perlu
        self.timestamp = str(timestamp)
        # Data diperlakukan sebagai JSON dan disimpan sebagai dict
        self.data = data
        # previous_hash disimpan sebagai string
        self.previous_hash = str(previous_hash)
        # Hitung hash dan simpan sebagai string
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        # Konversi data yang digunakan untuk hash ke string
        block_string = json.dumps({
            "vote_index": self.vote_index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }).encode()
        # Hitung hash dan konversi hasilnya ke string
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
        # Konversi nilai-nilai ke bentuk dictionary
        return {
            'vote_index': self.vote_index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'hash': self.hash
        }


class Blockchain:
    def __init__(self):
        self.chain = self.load_blocks_from_database()

    def load_blocks_from_database(self):
        cur.execute("SELECT * FROM blocks ORDER BY vote_index ASC")
        blocks = []
        for row in cur.fetchall():
            # Debugging: Cetak data setiap baris yang diambil dari database
            print(f"Debug: Row from database - vote_index: {row[0]}, timestamp: {row[1]}, data: {row[2]}, previous_hash: {row[3]}, hash: {row[4]}")
            vote_index = str(row[0])
            block_data = json.loads(row[2])
            block = Block(vote_index, row[1], block_data, row[3])
            block.hash = row[4]
            blocks.append(block)
        return blocks

    def validate_block(self, new_block):
        if len(self.chain) == 0:
            self.add_block(new_block)
            print("Voting berhasil ditambahkan (dari genesis)")
            return True

        last_block = self.chain[-1]

        calculated_hash = last_block.calculate_hash()
        print(f"Debug: calculated_hash: {calculated_hash}, last_block.hash: {last_block.hash}")

        if calculated_hash == last_block.hash:
            new_block.previous_hash = last_block.hash
            new_block.vote_index = str(int(last_block.vote_index) + 1)
            self.add_block(new_block)
            print("Voting berhasil ditambahkan")
            return True
        else:
            print("Hash tidak cocok pada blok terakhir. Menghapus blok terakhir...")
            print(f"Debug: Menghapus blok terakhir dengan vote_index: {last_block.vote_index}")
            self.remove_block(last_block.vote_index)
            self.chain = self.load_blocks_from_database()
            return self.validate_block(new_block)

    def remove_block(self, vote_index):
        vote_index = int(vote_index)
        block_to_remove = self.chain[vote_index]

        # Debugging: Cetak detail blok yang akan dihapus
        print(f"Debug: Menghapus blok dengan vote_index: {block_to_remove.vote_index}, hash: {block_to_remove.hash}")
        
        cur.execute("DELETE FROM blocks WHERE vote_index = %s", (block_to_remove.vote_index,))
        mydb.commit()
        del self.chain[vote_index]
        self.chain = self.load_blocks_from_database()

    def add_block(self, new_block):
        # Debugging: Cetak detail blok baru yang akan ditambahkan
        print(f"Debug: Menambahkan blok baru - vote_index: {new_block.vote_index}, timestamp: {new_block.timestamp}, data: {new_block.data}, previous_hash: {new_block.previous_hash}, hash: {new_block.hash}")
        
        cur.execute("""
        INSERT INTO blocks (vote_index, timestamp, data, previous_hash, hash)
        VALUES (%s, %s, %s, %s, %s)
        """, (new_block.vote_index, new_block.timestamp, json.dumps(new_block.data), new_block.previous_hash, new_block.hash))
        mydb.commit()
        self.chain = self.load_blocks_from_database()
