from flask import Blueprint, session, Response, current_app
import time
import json
import os
import sys
from module.db_utils import get_db

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','module')))

transaction_bp = Blueprint('transaction', __name__)

@transaction_bp.route("/transactions")
def transactions():
    if 'logged_in' in session and session['logged_in']:
        def generate():
            with current_app.app_context():
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
                    yield 'data: {}\n\n'.format(json.dumps(formatted_transactions))
                    time.sleep(1)
        return Response(generate(), content_type='text/event-stream')
    else:
        return '', 403
