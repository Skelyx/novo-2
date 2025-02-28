from flask import Flask
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

if __name__ == '__main__':
    db.create_all()
    app.run(host="0.0.0.0", port=10000, debug=True)
