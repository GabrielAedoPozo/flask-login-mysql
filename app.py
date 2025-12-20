from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
import mysql.connector
import uuid
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "clave_secreta_super_simple"
bcrypt = Bcrypt(app)

# ---------------- CONEXIÓN MYSQL ----------------
db = mysql.connector.connect(
    host="localhost",
    user="flaskuser",
    password="flaskpass123",
    database="login_db"
)

def send_email(to_email, link):
    try:
        msg = EmailMessage()
        msg["Subject"] = "Restablecer contraseña"
        msg["From"] = "aedothegabriel@gmail.com"
        msg["To"] = to_email
        msg.set_content(f"""
Hola,

Has solicitado restablecer tu contraseña.
Haz clic en el siguiente enlace:

{link}

Este enlace expira en 30 minutos.
""")

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as smtp:
            smtp.login(
                "aedothegabriel@gmail.com",
                "qqvy xlfq qdyv twik"  # app password con espacios
            )
            smtp.send_message(msg)

    except Exception as e:
        print("❌ ERROR AL ENVIAR EMAIL:", e)



# ---------------- HOME ----------------
@app.route('/')
def home():
    return redirect(url_for('login'))

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']

        cursor = db.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM users_new WHERE usuario=%s",
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

# ---------------- REGISTRO ----------------
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        email = request.form['email']
        contrasena = request.form['contrasena']

        cursor = db.cursor()
        cursor.execute(
            "SELECT id FROM users_new WHERE usuario=%s OR email=%s",
            (usuario, email)
        )

        if cursor.fetchone():
            cursor.close()
            flash("Usuario o correo ya existen")
            return redirect(url_for('registro'))

        hashed = bcrypt.generate_password_hash(contrasena).decode('utf-8')

        cursor.execute(
            "INSERT INTO users_new (usuario, email, password) VALUES (%s, %s, %s)",
            (usuario, email, hashed)
        )
        db.commit()
        cursor.close()

        flash("Cuenta creada correctamente")
        return redirect(url_for('login'))

    return render_template('register.html')

# ---------------- RECUPERAR CONTRASEÑA ----------------
@app.route('/recuperar-contrasena', methods=['GET', 'POST'])
def recuperar_contrasena():
    if request.method == 'POST':
        email = request.form['email']
        token = str(uuid.uuid4())
        expire = datetime.now() + timedelta(minutes=30)

        cursor = db.cursor()
        cursor.execute(
            "UPDATE users_new SET reset_token=%s, reset_token_expire=%s WHERE email=%s",
            (token, expire, email)
        )
        db.commit()

        if cursor.rowcount == 0:
            cursor.close()
            flash("Correo no encontrado")
            return redirect(url_for('recuperar_contrasena'))

        cursor.close()

        link = f"http://localhost:5000/restablecer-contrasena/{token}"
        send_email(email, link)

        flash("Revisa tu correo")
        return redirect(url_for('login'))

    return render_template('recuperar_contrasena.html')

# ---------------- RESTABLECER ----------------
@app.route('/restablecer-contrasena/<token>', methods=['GET', 'POST'])
def restablecer_contrasena(token):
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM users_new WHERE reset_token=%s AND reset_token_expire > NOW()",
        (token,)
    )
    user = cursor.fetchone()

    if not user:
        cursor.close()
        flash("Enlace inválido o expirado")
        return redirect(url_for('login'))

    if request.method == 'POST':
        nueva = request.form['nueva_contrasena']
        hashed = bcrypt.generate_password_hash(nueva).decode('utf-8')

        cursor.execute(
            "UPDATE users_new SET password=%s, reset_token=NULL, reset_token_expire=NULL WHERE id=%s",
            (hashed, user['id'])
        )
        db.commit()
        cursor.close()

        flash("Contraseña actualizada")
        return redirect(url_for('login'))

    cursor.close()
    return render_template('restablecer_contrasena.html')

# ---------------- PANEL ----------------
@app.route('/pagina_principal')
def pagina_principal():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', usuario=session['usuario'])

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
