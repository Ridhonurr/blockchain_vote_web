from flask import request, render_template, session,Blueprint, redirect, url_for
import os
import sys
from module.session import UserManager

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'module'))) ### menambahkan path module agar dapat memanggil module lain

index_bp = Blueprint('index',__name__)

@index_bp.route("/", methods=["GET", "POST"])
def index():
    user_manager = UserManager()
    if request.method == 'POST' and 'nis' in request.form and 'password' in request.form:
        nis = request.form['nis']
        password = request.form['password']
        user = user_manager.login(nis, password)
        error = False
        if user:
            session['logged_in'] = True
            session['nis'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('vote.vote'))
        else:
            error = True
            return render_template('index.html', error=error)
    return render_template('index.html')