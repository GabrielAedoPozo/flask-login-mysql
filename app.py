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
        return redirect(url_for('pagina_principal'))
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
            return redirect(url_for('pagina_principal'))
        else:
            flash("Usuario o contraseña incorrectos")

    return render_template('login.html')


@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        email = request.form['email']
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
            "INSERT INTO users (usuario, email, password) VALUES (%s, %s, %s)",
            (usuario, email, hashed)
        )
        db.commit()
        cursor.close()

        flash("Cuenta creada correctamente")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/pagina_principal')
def pagina_principal():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', usuario=session['usuario'])


@app.route('/mi_perfil')
def mi_perfil():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE usuario = %s", (session['usuario'],))
    user = cursor.fetchone()
    cursor.close()
    
    if user:
        return render_template('mi_perfil.html', usuario=user['usuario'], email=user.get('email', 'No disponible'))
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
