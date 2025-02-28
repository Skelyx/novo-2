import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Povezivanje sa MySQL bazom na Renderu
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:root@my-database-instance.onrender.com:3306/flask_app_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.urandom(24)  # Dodavanje ključ za sesije

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

# Homepage route
@app.route('/')
def index():
    return render_template('index.html')

# Submit route za login formu
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')

    # Provera da li korisnik postoji u bazi
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html', message="Invalid credentials, try again.")

# Dashboard route nakon uspešnog logovanja
@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

# Pokretanje aplikacije
if __name__ == '__main__':
    db.create_all()  # Kreira sve tabele ako ne postoje
    app.run(host="0.0.0.0", port=10000, debug=True)
