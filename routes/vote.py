from flask import Blueprint, session, url_for, redirect, request, render_template
import os
import sys
from module.voting import cek_pemilih, voting, list_kandidat
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..','module')))


vote_bp = Blueprint('vote', __name__)

@vote_bp.route("/vote", methods=['GET', 'POST'])
def vote():
    if 'username' in session:
        kandidat_list = list_kandidat()
        error = False
        print("Memproses permintaan di route '/vote'")
        if request.method == 'POST':
            nis = session['nis']
            pilihan = request.form['pilihan']
            user = cek_pemilih(nis)
            if user:
                error = True
                print(f"User pemilih: {user[1]}")
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
        return redirect(url_for('index.index'))
