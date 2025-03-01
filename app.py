from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# Povezivanje s bazom podataka
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definicija modela
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(200), nullable=False)


# Kreiranje tabela
with app.app_context():
    try:
        db.create_all()
        print("✅ Baza podataka je uspešno povezana i tabele su kreirane!")
    except Exception as e:
        print(f"❌ GREŠKA pri povezivanju na bazu: {e}")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Provera da li korisnik postoji u bazi
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            return "✅ Uspešno ste prijavljeni!"
        else:
            return render_template('index.html', message='❌ Neispravno korisničko ime ili lozinka')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=True)
