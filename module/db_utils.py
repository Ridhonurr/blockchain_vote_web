from flask import g
from .database import konekdb

def get_db():
    if 'db' not in g:
        g.db, g.cur = konekdb()
    return g.db, g.cur
