from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import mysql.connector

app = Flask(__name__)
app.secret_key = "clave_secreta_super_simple"
bcrypt = Bcrypt(app)

# ---------------- CONEXIÓN A MYSQL ----------------
db = mysql.connector.connect(
    host="localhost",
    user="flaskuser",          # usuario que creaste
    password="flaskpass123",   # contraseña que pusiste
    database="login_db"
)

# ---------------- RUTAS ----------------

@app.route('/')
def home():
    if 'usuario' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users WHERE usuario = %s",
            (usuario,)
        )
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.check_password_hash(user['password'], contrasena):
            session['usuario'] = usuario
            return redirect(url_for('dashboard'))
        else:
            flash("Usuario o contraseña incorrectos")

    return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        cursor = db.cursor()
        cursor.execute(
            "SELECT id FROM users WHERE usuario = %s",
            (usuario,)
        )

        if cursor.fetchone():
            cursor.close()
            flash("El usuario ya existe")
            return redirect(url_for('registro'))

        hashed = bcrypt.generate_password_hash(contrasena).decode('utf-8')

        cursor.execute(
            "INSERT INTO users (usuario, password) VALUES (%s, %s)",
            (usuario, hashed)
        )
        db.commit()
        cursor.close()

        flash("Cuenta creada correctamente")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return f"""
        <h1>Bienvenido {session['usuario']}</h1>
        <a href="/logout">Cerrar sesión</a>
    """


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
