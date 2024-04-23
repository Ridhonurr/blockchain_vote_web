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
            # Konversi vote_index ke str
            vote_index = str(row[0])
            # Parse data dari database menjadi dict
            block_data = json.loads(row[2])
            # Buat objek Block dengan data
            block = Block(vote_index, row[1], block_data, row[3])
            block.hash = row[4]
            blocks.append(block)
        return blocks

    def validate_block(self, new_block):
        # Periksa apakah ada blok sebelumnya
        if len(self.chain) == 0:
            # Jika self.chain adalah genesis (hanya memiliki 0 atau 1 blok), lewati validasi dan tambahkan blok baru
            self.add_block(new_block)
            print("Voting berhasil ditambahkan (dari genesis)")
            return True

        # Ambil blok terakhir dari chain
        last_block = self.chain[-1]

        # Hitung hash dari blok terakhir
        calculated_hash = last_block.calculate_hash()

        # Validasi hash dari blok terakhir
        if calculated_hash == last_block.hash:
            # Jika hash cocok, gunakan previous_hash dari blok terakhir untuk new_block
            new_block.previous_hash = last_block.hash
            # Set vote_index untuk new_block
            # Konversi last_block.vote_index ke str dan tambahkan 1
            new_block.vote_index = str(int(last_block.vote_index) + 1)
            # Tambahkan blok baru ke chain
            self.add_block(new_block)
            print("Voting berhasil ditambahkan")
            return True
        else:
            # Jika hash tidak cocok, hapus blok terakhir dan ulangi langkah validasi
            print("Hash tidak cocok pada blok terakhir. Menghapus blok terakhir...")
            # Hapus blok terakhir dan reset vote_index
            deleted_vote_index = last_block.vote_index
            self.remove_block(deleted_vote_index)
            # Ubah vote_index dari new_block menjadi vote_index dari blok yang dihapus
            new_block.vote_index = str(deleted_vote_index)
            # Memperbarui chain dari database
            self.chain = self.load_blocks_from_database()
            # Ulangi validasi dari atas dengan new_block yang telah diubah
            return self.validate_block(new_block)

    def remove_block(self, vote_index):
        # Hapus blok dari database dan chain
        vote_index = int(vote_index)
        block_to_remove = self.chain[vote_index]

        cur.execute("DELETE FROM blocks WHERE vote_index = %s", (block_to_remove.vote_index,))
        mydb.commit()
        del self.chain[vote_index]

    def add_block(self, new_block):
        # Tambahkan blok ke database dan chain
        cur.execute("""
        INSERT INTO blocks (vote_index, timestamp, data, previous_hash, hash)
        VALUES (%s, %s, %s, %s, %s)
        """, (new_block.vote_index, new_block.timestamp, json.dumps(new_block.data), new_block.previous_hash, new_block.hash))
        mydb.commit()
        self.chain.append(new_block)

