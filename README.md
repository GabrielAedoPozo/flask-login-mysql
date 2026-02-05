# 🔐 Login System con Flask y MySQL

Sistema completo de **autenticación** (registro, login, logout, recuperación de contraseña) desarrollado con **Flask** y **MySQL**. Soporta tanto autenticación tradicional como **Google OAuth 2.0**.

---

## ✨ Características

### Autenticación Tradicional
- ✅ Registro de usuarios con email único
- ✅ Inicio de sesión con usuario y contraseña
- ✅ Hash de contraseñas con `Flask-Bcrypt`
- ✅ Cierre de sesión (logout)
- ✅ Manejo seguro de sesiones con Flask

### Google OAuth 2.0
- ✅ Login con Google (solo usuarios existentes)
- ✅ Registro con Google (crear cuenta automáticamente)
- ✅ Validación de tokens con `google-auth`
- ✅ Almacenamiento de ID de Google y foto de perfil

### Recuperación de Contraseña
- ✅ Solicitud de restablecimiento por email
- ✅ Tokens únicos con expiración (30 minutos)
- ✅ Envío de emails con `smtplib` (Gmail)
- ✅ Actualización segura de contraseña

### General
- ✅ Base de datos MySQL
- ✅ Gestión de usuario y perfil
- ✅ Vistas responsive con `templates/` y assets en `static/`
- ✅ Manejo de errores y validaciones

---

## Requisitos

- Python 3.10+ (recomendado)
- MySQL Server 8.x
- Pip

---

## 📁 Estructura del proyecto

```
.
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── mi_perfil.html
│   ├── recuperar_contrasena.html
│   ├── register.html
│   └── restablecer_contrasena.html
└── static/
    ├── app.js
    ├── contrasena.css
    ├── index.css
    ├── perfil.css
    ├── restablecer.css
    └── styles.css
```

---

## ⚙️ Instalación

### 1) Clonar el repo

```bash
git clone https://github.com/GabrielAedoPozo/flask-login-mysql.git
cd flask-login-mysql
```

### 2) Crear y activar entorno virtual

**Windows (PowerShell):**
```bash
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## 🗄️ MySQL: creación de BD y tabla

1) Asegúrate de tener MySQL Server corriendo.
2) Crea la base de datos y tabla ejecutando [`update_database.sql`](update_database.sql):

```bash
mysql -u flaskuser -p flaskpass123 login_db < update_database.sql
```

O manualmente:

```sql
CREATE DATABASE IF NOT EXISTS login_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE login_db;

CREATE TABLE IF NOT EXISTS users_new (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255),
    google_id VARCHAR(255) UNIQUE,
    picture TEXT,
    auth_provider VARCHAR(50),
    reset_token VARCHAR(255),
    reset_token_expire DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Configuración de conexión

**IMPORTANTE**: Las credenciales de MySQL NO deben estar en el código.

Crea un archivo `.env` en la raíz con:

```env
DB_HOST=localhost
DB_USER=flaskuser
DB_PASSWORD=tu_contraseña_mysql
DB_NAME=login_db
```

El código usa `python-dotenv` para cargar estas variables:

```python
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
```

> Nota: Este proyecto usa el driver **mysql-connector-python** (incluido en [`requirements.txt`](requirements.txt)).

---

## 🔑 Google OAuth 2.0: Configuración

### 1) Obtener credenciales de Google

1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un proyecto nuevo
3. Habilita la API **Google+ API**
4. Crea un ID de Cliente OAuth 2.0 (tipo: Aplicación web)
5. Añade `http://localhost:5000` como JavaScript origin
6. Copia el **Client ID**

### 2) Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto (ver `.env.example` para plantilla):

```env
GOOGLE_CLIENT_ID=tu_google_client_id_aqui.apps.googleusercontent.com
SECRET_KEY=tu_clave_secreta_muy_larga_aqui
```

Este archivo es **privado** y no debe commitirse a Git (está en `.gitignore`).

### 3) Endpoints de Google OAuth

- **Login**: `POST /auth/google` - Autentica usuario existente
- **Registro**: `POST /auth/google/register` - Crea nuevo usuario

---

## 📧 Email: Configuración para recuperación de contraseña

### 1) Generar contraseña de aplicación en Gmail

1. Activa la **verificación en dos pasos** en tu cuenta de Gmail
2. Ve a [Contraseñas de aplicación](https://myaccount.google.com/apppasswords)
3. Genera una contraseña para "Correo"
4. Copia la contraseña de 16 caracteres

### 2) Configurar variables de entorno

Añade al archivo `.env`:

```env
EMAIL_SENDER=tu_email@gmail.com
EMAIL_PASSWORD=contraseña_de_aplicación_16_caracteres
APP_HOST=https://tudominio.com  # Para producción
```

Las credenciales se cargan de forma segura desde `.env`.

---

## 🔗 Rutas de la Aplicación

| Ruta | Método | Descripción |
|------|--------|------------|
| `/` | GET | Redirige a login |
| `/login` | GET, POST | Página y procesamiento de login |
| `/registro` | GET, POST | Página y procesamiento de registro |
| `/recuperar-contrasena` | GET, POST | Solicitud de token de restablecimiento |
| `/restablecer-contrasena/<token>` | GET, POST | Página para establecer nueva contraseña |
| `/pagina_principal` | GET | Panel principal (requiere sesión) |
| `/mi_perfil` | GET | Perfil del usuario (requiere sesión) |
| `/logout` | GET | Cierra sesión |
| `/auth/google` | POST | Login con Google OAuth |
| `/auth/google/register` | POST | Registro con Google OAuth |

---

## ▶️ Ejecutar el proyecto

### Antes de iniciar

Asegúrate de tener:
- ✅ MySQL corriendo
- ✅ Variables de entorno configuradas (`.env`)
- ✅ Dependencias instaladas (`pip install -r requirements.txt`)

### Iniciar la aplicación

Con el entorno virtual activado:

```bash
py app.py
```

Luego abre en tu navegador:

- **http://127.0.0.1:5000**

---

## 🔐 Seguridad

### Medidas implementadas:
- ✅ Contraseñas hasheadas con bcrypt (nunca en texto plano)
- ✅ Tokens CSRF implícitos en sesiones Flask
- ✅ Validación de tokens de Google OAuth con certificados oficiales
- ✅ Tokens de restablecimiento únicos y con expiración (30 minutos)
- ✅ Protección de rutas requiriendo sesión activa
- ✅ Credenciales en variables de entorno (`.env` - no en Git)
- ✅ Debug mode desactivado en producción

### Configuración de seguridad para producción:

1. **Cambiar SECRET_KEY**:
   ```env
   SECRET_KEY=generar_nueva_clave_secreta_aleatoria_de_32_caracteres
   ```

2. **Configurar HTTPS**:
   ```env
   APP_HOST=https://tudominio.com
   FLASK_ENV=production
   ```

3. **Usar base de datos remota** (no localhost):
   ```env
   DB_HOST=servidor-mysql.tudominio.com
   ```

4. **Variables de entorno requeridas**:
   - `SECRET_KEY` - Clave secreta (generar con `secrets.token_urlsafe(32)`)
   - `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
   - `GOOGLE_CLIENT_ID`
   - `EMAIL_SENDER`, `EMAIL_PASSWORD`
   - `FLASK_ENV=production`

---

## 📦 Dependencias

```
Flask
Flask-Bcrypt
mysql-connector-python
google-auth
python-dotenv
```

Ver [`requirements.txt`](requirements.txt) para versiones específicas.

---

## 📝 Notas

- La aplicación usa **MySQL** como base de datos
- Los emails se envían mediante **Gmail SMTP**
- **Google OAuth** requiere credenciales del Google Cloud Console
- Archivos sensibles (`.env`) se deben añadir a `.gitignore`

---

## 📄 Licencia

Este proyecto está disponible bajo licencia MIT.
