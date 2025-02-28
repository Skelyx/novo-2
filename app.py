import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Dobijanje DATABASE_URL iz Railway okruženja ili korišćenje podrazumevanog
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:YITSMKJBsmZXowpMgMynhHMwJijxIYUD@shinkansen.proxy.rlwy.net:11774/railway')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
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

# Početna stranica
@app.route('/')
def index():
    return render_template('index.html')

# Ruta za prijavu
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()
    
    if user and user.check_password(password):
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html', message="Invalid credentials, try again.")

# Dashboard
@app.route('/dashboard')
def dashboard():
    return "Welcome to the dashboard!"

# Kreiranje tabela u bazi ako ne postoje
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
