import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Povezivanje sa Railway MySQL bazom
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:aiBzbPEEvtrurGaPrXjVZWgdVDjgABbt@maglev.proxy.rlwy.net:50172/railway')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True  # Prikaz SQL upita u konzoli
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

# Model za korisnike
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)  # Hashirane lozinke mogu biti duže

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<User {self.username}>'


# Homepage
@app.route('/')
def index():
    return render_template('index.html')


# Registracija korisnika
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash("Morate uneti korisničko ime i lozinku!", "danger")
        return redirect(url_for('index'))

    # Provera da li korisnik već postoji
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        flash("Korisničko ime već postoji!", "danger")
        return redirect(url_for('index'))

    # Kreiranje novog korisnika
    new_user = User(username=username)
    new_user.set_password(password)

    try:
        db.session.add(new_user)
        db.session.commit()
        flash("Registracija uspešna! Možete se prijaviti.", "success")
    except Exception as e:
        db.session.rollback()
        print("GREŠKA PRI UPISU:", str(e))
        flash("Greška pri registraciji, pokušajte ponovo.", "danger")

    return redirect(url_for('index'))


# Login korisnika
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    print(f"Form data: {request.form}")  # Debug print

    user = User.query.filter_by(username=username).first()
    if not user:
        print(f"Korisnik {username} NIJE pronađen u bazi.")
        flash("Pogrešno korisničko ime ili lozinka.", "danger")
        return redirect(url_for('index'))

    if user.check_password(password):
        print(f"Uspešna prijava korisnika {username}")
        flash("Uspešno ste prijavljeni!", "success")
        return redirect(url_for('dashboard'))
    else:
        print(f"Neuspešna prijava za korisnika {username} - lozinka netačna!")
        flash("Pogrešno korisničko ime ili lozinka.", "danger")
        return redirect(url_for('index'))


# Dashboard
@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"


# Kreiranje tabela (samo prvi put)
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    print("DATABASE URL:", app.config['SQLALCHEMY_DATABASE_URI'])  # Provera URL-a
    app.run(host="0.0.0.0", port=10000, debug=True)
