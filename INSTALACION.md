# 🔐 CONFIGURACIÓN INICIAL - Para quién clona este repo

Sigue estos pasos para ejecutar el proyecto de forma segura:

## 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/p-gina-login.git
cd p-gina-login
```

## 2. Crear entorno virtual

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

## 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

## 4. Configurar variables de entorno

**Copiar el archivo de plantilla:**
```bash
cp .env.example .env
```

**Editar `.env` con tus valores:**

```env
# Generar con: python -c "import secrets; print(secrets.token_urlsafe(32))"
SECRET_KEY=TU_CLAVE_SECRETA_GENERADA_AQUI

# Base de datos MySQL
DB_HOST=localhost
DB_USER=tu_usuario_mysql
DB_PASSWORD=tu_contraseña_mysql
DB_NAME=login_db

# Google OAuth (obtener en https://console.cloud.google.com)
GOOGLE_CLIENT_ID=tu-client-id.apps.googleusercontent.com

# Gmail (obtener App Password en https://myaccount.google.com/apppasswords)
EMAIL_SENDER=tu-email@gmail.com
EMAIL_PASSWORD=tu-app-password-16-caracteres

# Configuración local
FLASK_ENV=development
APP_HOST=http://localhost:5000
```

## 5. Crear base de datos MySQL

**Opción A: Ejecutar script SQL**
```bash
mysql -u tu_usuario -p tu_contraseña login_db < update_database.sql
```

**Opción B: Manualmente en MySQL**
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

## 6. Ejecutar la aplicación

```bash
python app.py
```

Abre en tu navegador: **http://localhost:5000**

---

## ⚠️ IMPORTANTE - SEGURIDAD

- ✅ El archivo `.env` NO se sube a Git
- ✅ Nunca commits tus credenciales
- ✅ Usa credenciales diferentes para cada entorno (dev/prod)
- ✅ En producción: HTTPS obligatorio

Ver [SECURITY_CHECKLIST.md](SECURITY_CHECKLIST.md) para más detalles.
