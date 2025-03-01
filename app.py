import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# ✅ Railway MySQL konekcija
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:aiBzbPEEvtrurGaPrXjVZWgdVDjgABbt@maglev.proxy.rlwy.net:50172/railway')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

# ✅ Model korisnika (Users)
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'

# ✅ Model za beleženje pokušaja prijave (Login Attempts)
class LoginAttempt(db.Model):
    __tablename__ = 'login_attempts'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)  # Čuva plaintext šifru za analizu napada
    success = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<LoginAttempt {self.username} - {"Success" if self.success else "Failed"}>'

# ✅ Kreiranje tabela
with app.app_context():
    try:
        db.create_all()
        print("✅ Baza podataka je uspešno povezana i tabele su kreirane!")
        
        # 🔍 Provera trenutne baze
        result = db.engine.execute("SELECT DATABASE();").fetchone()
        print(f"📌 Trenutno koristiš bazu: {result[0]}")
    
    except Exception as e:
        print(f"❌ GREŠKA pri povezivanju na bazu: {e}")

# ✅ Početna strana
@app.route('/')
def index():
    return render_template('index.html')

# ✅ Registracija korisnika
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Sva polja su obavezna!", "danger")
            return redirect(url_for('register'))

        # Provera da li korisnik već postoji
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Korisničko ime već postoji!", "danger")
            return redirect(url_for('register'))

        # Kreiranje novog korisnika
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Uspešno ste registrovani!", "success")
        return redirect(url_for('index'))

    return render_template('register.html')

# ✅ Login korisnika (čuva pokušaje u `login_attempts`)
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    print(f"🔍 Pokušaj prijave: {username}")

    # Provera korisnika u bazi
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # 🔹 Čuvanje uspešnog pokušaja u `login_attempts`
        attempt = LoginAttempt(username=username, password=password, success=True)
        db.session.add(attempt)
        db.session.commit()

        flash("✅ Uspešno ste prijavljeni!", "success")
        return redirect(url_for('dashboard'))
    
    else:
        # 🔹 Čuvanje neuspešnog pokušaja u `login_attempts`
        attempt = LoginAttempt(username=username, password=password, success=False)
        db.session.add(attempt)
        db.session.commit()

        flash("❌ Neispravno korisničko ime ili lozinka!", "danger")
        return redirect(url_for('index'))

# ✅ Dashboard
@app.route('/dashboard')
def dashboard():
    return "🚀 Dobrodošli na Dashboard!"

# ✅ Pokretanje aplikacije
if __name__ == '__main__':
    print("DATABASE URL:", app.config['SQLALCHEMY_DATABASE_URI'])  # Provera URL-a baze
    app.run(host="0.0.0.0", port=10000, debug=True)
