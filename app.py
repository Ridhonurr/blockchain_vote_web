from flask import Flask, render_template, url_for, session,redirect, request, Response
from module.voting import list_kandidat, cek_pemilih, voting
from module.session import UserManager
from module.database import konekdb
import time
import json

mydb, cur = konekdb()

app = Flask(__name__)
app.secret_key = 'bec0013002756f5467d5883541b1d04e1eb823316554f6610caca4ef13485d81'

@app.route("/", methods=["GET","POST"])
def index():
    user_manager = UserManager()
    if request.method == 'POST' and 'nis' in request.form and 'password' in request.form:
        nis = request.form['nis']
        password = request.form['password']
        user = user_manager.login(nis,password)
        error = False
        if user:
            session['logged_in'] = True
            session['nis'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('vote'))
        else:
            error = True
            return render_template('index.html', error=error)
    return render_template('index.html')

@app.route("/vote", methods=['GET', 'POST'])
def vote():
    if 'username' in session:
        kandidat_list = list_kandidat()
        error = False
        print("Memproses permintaan di route '/vote'")
        if request.method == 'POST':
            nis = session['nis']
            pilihan = request.form['pilihan']
            user = cek_pemilih(nis)
            print(f"User pemilih: {user[1]}")
            if user:
                error = True
                print(f"Pemilih telah memilih sebelumnya: {user[2]}")
                return render_template('voting.html', error=error, list=kandidat_list)
            else:
                voting(nis, pilihan)
                berhasil = 'berhasil'
                print("Pemilih berhasil memilih.")
                return render_template('voting.html', berhasil=berhasil, list=kandidat_list)
        return render_template('voting.html', list=kandidat_list)
    else:
        print("Pengguna belum login, mengarahkan ke halaman login.")
        return redirect(url_for('index'))
    

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('nis', None)
    session.pop('logged_in', False)
    return redirect(url_for('index'))

# Endpoint untuk menampilkan data transaksi secara real-time
# Endpoint untuk menampilkan data transaksi secara real-time
@app.route("/transactions")
def transactions():
    if 'logged_in' in session and session['logged_in']:
        def generate():
            while True:
                # Ambil data transaksi dari database (contoh: pengambilan 10 transaksi terbaru)
                cur.execute("SELECT * FROM blocks ORDER BY vote_index DESC LIMIT 10")
                transactions = cur.fetchall()

                # Format output data transaksi
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

                # Kirim data transaksi sebagai Server-Sent Events
                yield 'data: {}\n\n'.format(json.dumps(formatted_transactions))

                # Biarkan proses menunggu sebelum mengambil transaksi berikutnya
                time.sleep(1)  # Misalnya, tunggu 1 detik sebelum mengambil data lagi

        return Response(generate(), content_type='text/event-stream')
    else:
        return '', 403

