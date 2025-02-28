from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Povezivanje sa MySQL bazom
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/flask_app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model za korisnike
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Ruta za početnu stranicu
@app.route('/')
def index():
    return render_template('index.html')

# Ruta za prijavu
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form['username']
    password = request.form['password']

    # Dodaj korisnika u bazu
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()

    # Prikazivanje poruke
    return render_template('index.html', message="Uspješno ste se prijavili!")

if __name__ == '__main__':
    db.create_all()
    app.run(host="0.0.0.0", port=10000, debug=True)
