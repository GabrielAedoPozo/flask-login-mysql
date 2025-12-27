# 🔐 Login System con Flask y MySQL

Sistema de **autenticación** (registro, login, logout y sesiones) desarrollado con **Flask** y **MySQL**, enfocado en una estructura simple para portafolio.

Este proyecto es una adaptación de una versión previa con MongoDB, migrado para usar **MySQL** como persistencia.

---

## Características

- Registro de usuarios
- Inicio de sesión (login)
- Cierre de sesión (logout)
- Hash de contraseñas con `Flask-Bcrypt`
- Manejo de sesiones con Flask
- Base de datos MySQL (driver `mysql-connector-python`)
- Vistas con `templates/` y assets en `static/`

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

1) Asegúrate de tener MySQL corriendo.
2) Crea la base de datos y tabla:

```sql
CREATE DATABASE IF NOT EXISTS login_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE login_db;

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL
);
```

### Configuración de conexión
Configura las credenciales de MySQL en el archivo [`app.py`](app.py) (host, usuario, contraseña y base de datos) para que coincidan con tu instalación local.

> Nota: Este proyecto usa el driver **mysql-connector-python** (incluido en [`requirements.txt`](requirements.txt)).

---

## ▶️ Ejecutar el proyecto

Con el entorno virtual activado:

```bash
py app.py
```

Luego abre:

- http://127.0.0.1:5000

---

## 🔐 Seguridad (básica)

- Las contraseñas no se guardan en texto plano (hash con bcrypt)
- Sesiones para proteger rutas

---

## Estado

✅ Funcional  
🔜 Mejoras posibles: validaciones, roles, deploy
