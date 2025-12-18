# 🔐 Login System con Flask y MySQL

Proyecto de **sistema de autenticación** (registro, login y sesiones) desarrollado con **Flask** y **MySQL**, enfocado en buenas prácticas de backend, seguridad básica y estructura profesional para portafolio.

Este proyecto es una **adaptación y mejora de un proyecto base originalmente implementado con MongoDB**, el cual fue **modificado completamente para utilizar MySQL**, manteniendo la lógica de autenticación pero cambiando la capa de persistencia de datos.

---

##  Características

* Registro de usuarios
* Inicio de sesión (login)
* Cierre de sesión (logout)
* Contraseñas **hasheadas** con `flask-bcrypt`
* Manejo de sesiones con Flask
* Base de datos MySQL
* Arquitectura clara (`templates` / `static`)

---

## 🛠️ Tecnologías usadas

* **Python 3**
* **Flask**
* **MySQL**
* **mysql-connector-python**
* **Flask-Bcrypt**
* HTML5 / CSS3

---

## 📁 Estructura del proyecto

```
flask-login-mysql/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── templates/
│   ├── login.html
│   ├── register.html
│   └── index.html
│
└── static/
    ├── styles.css
    └── app.js
```

---

## ⚙️ Instalación y configuración

### 1️ Clonar el repositorio

```bash
git clone https://github.com/GabrielAedoPozo/flask-login-mysql.git
cd flask-login-mysql
```

### 2️ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3️ Crear la base de datos en MySQL

```sql
CREATE DATABASE login_db;

USE login_db;

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario VARCHAR(100) NOT NULL UNIQUE,
    email VARCHAR(150) NOT NULL UNIQUE,
    contrasena VARCHAR(255) NOT NULL
);
```

---

##  Ejecutar el proyecto

```bash
py app.py
```

Luego abre en tu navegador:

```
http://127.0.0.1:5000
```

---

## 🔐 Seguridad

* Las contraseñas **NO se guardan en texto plano**
* Se usa hash seguro con `bcrypt`
* Uso de sesiones para proteger rutas

---

##  Estado del proyecto

✅ Funcional

🔜 Posibles mejoras futuras:

* Recuperación de contraseña por email
* Roles de usuario
* Validaciones avanzadas
* Deploy en producción

---

## 🔄 Adaptación del proyecto

* Proyecto base originalmente desarrollado con **MongoDB**
* Migración completa a **MySQL** usando `mysql-connector

**Gabriel Aedo Pozo**
Desarrollador web en formación, enfocado en backend y fullstack.

* GitHub: [https://github.com/GabrielAedoPozo](https://github.com/GabrielAedoPozo)

---

⭐ Si te gusta el proyecto, ¡dale una estrella!
⭐ Proximas Actualizaciones!!!!!!
