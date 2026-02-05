from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_bcrypt import Bcrypt
import mysql.connector
import uuid
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

load_dotenv()

# Configurar Client ID de Google OAuth (debe estar en .env)
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")


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
        print(" ERROR AL ENVIAR EMAIL:", e)



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

    # Pasar GOOGLE_CLIENT_ID al template
    return render_template('login.html', google_client_id=GOOGLE_CLIENT_ID)

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

    # Pasar GOOGLE_CLIENT_ID al template
    return render_template('register.html', google_client_id=GOOGLE_CLIENT_ID)

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

# ---------------- PERFIL ----------------
@app.route('/mi_perfil')
def mi_perfil():
    if 'usuario' not in session:
        return redirect(url_for('login'))

    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT email FROM users_new WHERE usuario=%s",
        (session['usuario'],)
    )
    row = cursor.fetchone()
    cursor.close()

    email = row['email'] if row else ''
    return render_template('mi_perfil.html', usuario=session['usuario'], email=email)

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ---------------- GOOGLE OAUTH 2.0 ----------------
@app.route('/auth/google', methods=['POST'])
def auth_google():
    """
    Endpoint para autenticación (LOGIN) con Google OAuth 2.0
    Recibe idToken desde el frontend y valida el usuario
    Solo crea sesión si el usuario YA EXISTE
    """
    try:
        # Obtener el token desde el body de la petición
        data = request.get_json()
        token = data.get('idToken')
        
        if not token:
            return jsonify({'error': 'Token no proporcionado'}), 400
        
        # Validar el token con Google
        idinfo = id_token.verify_oauth2_token(
            token, 
            google_requests.Request(), 
            GOOGLE_CLIENT_ID
        )
        
        # Verificar que el token es válido para nuestra app
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return jsonify({'error': 'Token inválido'}), 401
        
        # Extraer información del usuario
        email = idinfo.get('email')
        name = idinfo.get('name')
        picture = idinfo.get('picture')
        google_id = idinfo.get('sub')  # ID único de Google
        
        if not email:
            return jsonify({'error': 'Email no disponible'}), 400
        
        cursor = db.cursor(dictionary=True)
        
        # Buscar usuario por email
        cursor.execute(
            "SELECT * FROM users_new WHERE email=%s",
            (email,)
        )
        user = cursor.fetchone()
        
        if user:
            # Usuario existe - actualizar google_id si no lo tiene
            if not user.get('google_id'):
                cursor.execute(
                    "UPDATE users_new SET google_id=%s, picture=%s, auth_provider='google' WHERE id=%s",
                    (google_id, picture, user['id'])
                )
                db.commit()
            
            # Crear sesión Flask
            session['usuario'] = user['usuario']
            cursor.close()
            
            return jsonify({
                'success': True,
                'message': 'Login exitoso',
                'usuario': user['usuario']
            }), 200
        
        else:
            # Usuario NO existe - no permitir login, debe registrarse
            cursor.close()
            return jsonify({
                'success': False,
                'error': 'Usuario no existe. Por favor regístrate primero.'
            }), 404
    
    except ValueError as e:
        # Token inválido o expirado
        return jsonify({'error': f'Token inválido: {str(e)}'}), 401
    
    except Exception as e:
        # Error general
        print("❌ ERROR EN GOOGLE LOGIN:", e)
        return jsonify({'error': 'Error en la autenticación'}), 500


@app.route('/auth/google/register', methods=['POST'])
def auth_google_register():
    """
    Endpoint para REGISTRO con Google OAuth 2.0
    Recibe idToken, valida y crea nuevo usuario si no existe
    """
    try:
        # Obtener el token desde el body de la petición
        data = request.get_json()
        token = data.get('idToken')
        
        if not token:
            return jsonify({'error': 'Token no proporcionado'}), 400
        
        # Validar el token con Google
        idinfo = id_token.verify_oauth2_token(
            token, 
            google_requests.Request(), 
            GOOGLE_CLIENT_ID
        )
        
        # Verificar que el token es válido para nuestra app
        if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return jsonify({'error': 'Token inválido'}), 401
        
        # Extraer información del usuario
        email = idinfo.get('email')
        name = idinfo.get('name')
        picture = idinfo.get('picture')
        google_id = idinfo.get('sub')  # ID único de Google
        
        if not email or not name:
            return jsonify({'error': 'Email o nombre no disponibles'}), 400
        
        cursor = db.cursor(dictionary=True)
        
        # Buscar si el usuario ya existe
        cursor.execute(
            "SELECT * FROM users_new WHERE email=%s",
            (email,)
        )
        user = cursor.fetchone()
        
        if user:
            # El email ya existe
            cursor.close()
            return jsonify({
                'success': False,
                'error': 'Este correo electrónico ya está registrado'
            }), 409
        
        # Crear nuevo usuario con Google OAuth
        try:
            cursor.execute(
                """INSERT INTO users_new 
                   (usuario, email, google_id, picture, password, auth_provider) 
                   VALUES (%s, %s, %s, %s, NULL, 'google')""",
                (name, email, google_id, picture)
            )
            db.commit()
            
            # Crear sesión Flask
            session['usuario'] = name
            cursor.close()
            
            return jsonify({
                'success': True,
                'message': 'Usuario registrado y login exitoso',
                'usuario': name
            }), 201
        
        except mysql.connector.Error as db_error:
            db.rollback()
            cursor.close()
            print("❌ ERROR EN BASE DE DATOS:", db_error)
            return jsonify({'error': 'Error al registrar usuario'}), 500
    
    except ValueError as e:
        # Token inválido o expirado
        return jsonify({'error': f'Token inválido: {str(e)}'}), 401
    
    except Exception as e:
        # Error general
        print("❌ ERROR EN GOOGLE REGISTER:", e)
        return jsonify({'error': 'Error en el registro'}), 500

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
