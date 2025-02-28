import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Povezivanje sa Railway MySQL bazom
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:aiBzbPEEvtrurGaPrXjVZWgdVDjgABbt@maglev.proxy.rlwy.net:50172/railway')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

# Model za korisnike
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

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

# Submit forma
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')

    print(f"Form data: {request.form}")  # Ovo prikazuje sve podatke iz forme
    print(f"Pokušaj prijave za korisnika: {username} sa lozinkom: {password}")

    # Provera da li korisnik postoji u bazi
    user = User.query.filter_by(username=username).first()
    if user:
        print(f"Korisnik pronađen: {user.username}")
    else:
        print(f"Korisnik sa username {username} NIJE pronađen u bazi!")

    # Provera lozinke
    if user and user.check_password(password):
        print("Uspešna prijava!")
        return redirect(url_for('dashboard'))
    else:
        print(f"Neuspešna prijava za korisnika {username} - lozinka netačna!")
        return render_template('index.html', message="Invalid credentials, try again.")

# Dashboard
@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

# Kreiranje tabela (samo prvi put)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print("DATABASE URL:", app.config['SQLALCHEMY_DATABASE_URI'])  # Proveri da li je URL tačan
    app.run(host="0.0.0.0", port=10000, debug=True)
