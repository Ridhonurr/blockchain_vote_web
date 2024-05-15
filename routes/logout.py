from flask import Blueprint, session,redirect,url_for

logout_bp = Blueprint('logout',__name__)

@logout_bp.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('nis', None)
    session.pop('logged_in', False)
    return redirect(url_for('index.index'))