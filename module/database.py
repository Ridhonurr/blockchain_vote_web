import mysql.connector as mysql
from dotenv import load_dotenv
import os

load_dotenv()
SERVER = os.getenv("SERVERDB")
USERNAMEDB = os.getenv("USERNAMEDB")
PASSDB = os.getenv("PASSDB")
DATABASE = os.getenv("DATABASE")
PORTDB=os.getenv("PORTDB")

def konekdb():
    try:
        mydb = mysql.connect(
            host=SERVER,
            user=USERNAMEDB,
            password=PASSDB,
            database=DATABASE,
            port=PORTDB
        )
        cur = mydb.cursor()
        return mydb,cur
    except mysql.Error as e:
        print(f"Error: {e}")
        return None,None