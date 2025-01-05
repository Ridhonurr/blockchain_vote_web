###### Module
from flask import Flask, g, session, Response
from module.db_utils import get_db
import ujson
import time
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("secret")
###### import blueprint
from routes.index import index_bp
from routes.vote import vote_bp
from routes.logout import logout_bp


app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.before_request
def before_request():
    get_db()

@app.teardown_request
def teardown_request(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

app.register_blueprint(index_bp)
app.register_blueprint(vote_bp)
app.register_blueprint(logout_bp)

@app.route("/transactions")
def transactions():
    if 'logged_in' in session and session['logged_in']:
        def generate():
            with app.app_context():
                while True:
                    db, cur = get_db()
                    cur.execute("SELECT * FROM blocks ORDER BY vote_index DESC LIMIT 10")
                    transactions = cur.fetchall()
                    formatted_transactions = []
                    for transaction in transactions:
                        formatted_transaction = {
                            'Vote Index': transaction[0],
                            'Timestamp': transaction[1],
                            'Data': transaction[2],
                            'Previous Hash': transaction[3],
                            'Hash': transaction[4]
                        }
                        formatted_transactions.append(formatted_transaction)
                    yield 'data: {}\n\n'.format(ujson.dumps(formatted_transactions))
                    time.sleep(1)
        return Response(generate(), content_type='text/event-stream')
    else:
        return '', 403


if __name__ == "__main__":
    app.run(debug=True)
