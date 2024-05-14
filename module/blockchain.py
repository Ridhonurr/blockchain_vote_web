import hashlib
import json
from .database import konekdb
import datetime
from flask import g

def get_db():
    if 'db' not in g:
        g.db, g.cur = konekdb()
    return g.db, g.cur

class Block:
    def __init__(self, vote_index, timestamp, data, previous_hash):
        self.vote_index = str(vote_index)
        self.timestamp = str(timestamp)
        self.data = data
        self.previous_hash = str(previous_hash)
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "vote_index": self.vote_index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }).encode()
        return hashlib.sha256(block_string).hexdigest()

    def to_dict(self):
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
        db, cur = get_db()
        cur.execute("SELECT * FROM blocks ORDER BY vote_index ASC")
        blocks = []
        for row in cur.fetchall():
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
        if calculated_hash == last_block.hash:
            new_block.previous_hash = last_block.hash
            new_block.vote_index = str(int(last_block.vote_index) + 1)
            self.add_block(new_block)
            print("Voting berhasil ditambahkan")
            return True
        else:
            print("Hash tidak cocok pada blok terakhir. Menghapus blok terakhir...")
            self.remove_block(last_block.vote_index)
            self.chain = self.load_blocks_from_database()
            return self.validate_block(new_block)

    def remove_block(self, vote_index):
        db, cur = get_db()
        vote_index = int(vote_index)
        cur.execute("DELETE FROM blocks WHERE vote_index = %s", (vote_index,))
        db.commit()
        self.chain = self.load_blocks_from_database()

    def add_block(self, new_block):
        db, cur = get_db()
        cur.execute("""
        INSERT INTO blocks (vote_index, timestamp, data, previous_hash, hash)
        VALUES (%s, %s, %s, %s, %s)
        """, (new_block.vote_index, new_block.timestamp, json.dumps(new_block.data), new_block.previous_hash, new_block.hash))
        db.commit()
        self.chain = self.load_blocks_from_database()
