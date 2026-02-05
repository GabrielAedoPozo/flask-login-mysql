# 🔒 SECURITY CHECKLIST - ANTES DE SUBIR A REPO PÚBLICO

## ✅ Problemas Corregidos:

### 1. **Credenciales Hardcodeadas** ✓
   - ❌ ANTES: `app.secret_key = "clave_secreta_super_simple"` en app.py
   - ✅ AHORA: Cargada desde `.env` con validación
   
### 2. **Credenciales MySQL** ✓
   - ❌ ANTES: host="localhost", user="flaskuser", password="flaskpass123"
   - ✅ AHORA: Todas en `.env` como variables de entorno

### 3. **Email de Usuario Expuesto** ✓
   - ❌ ANTES: "aedothegabriel@gmail.com" en código
   - ✅ AHORA: `EMAIL_SENDER` en `.env`

### 4. **Password de Gmail Expuesta** ✓
   - ❌ ANTES: Contraseña visible en comentario
   - ✅ AHORA: `EMAIL_PASSWORD` en `.env`

### 5. **Debug Mode Activo** ✓
   - ❌ ANTES: `app.run(debug=True)`
   - ✅ AHORA: Controlado por variable `FLASK_ENV` en `.env`

### 6. **URL Hardcodeada** ✓
   - ❌ ANTES: `http://localhost:5000` en recuperación de contraseña
   - ✅ AHORA: `APP_HOST` en `.env` (configurable para producción)

---

## 📋 REQUISITOS ANTES DE SUBIR:

### 1. Crear archivo `.env` local (NO se sube a Git)
   ```bash
   cp .env.example .env
   # Editar .env con tus valores reales
   ```

### 2. Verificar `.gitignore` contiene:
   ```
   .env
   .env.local
   __pycache__/
   *.pyc
   ```
   ✓ YA CONFIGURADO

### 3. Variables de entorno REQUERIDAS en `.env`:
   ```
   SECRET_KEY=generar_con_secrets.token_urlsafe(32)
   DB_HOST=localhost
   DB_USER=tu_usuario_mysql
   DB_PASSWORD=tu_contraseña_mysql
   DB_NAME=login_db
   GOOGLE_CLIENT_ID=tu_id_de_google
   EMAIL_SENDER=tu_email@gmail.com
   EMAIL_PASSWORD=tu_app_password_16_caracteres
   FLASK_ENV=production (en producción)
   APP_HOST=https://tudominio.com (en producción)
   ```

### 4. Verificar en GitHub:
   - [ ] No aparecen credenciales en commits
   - [ ] `.env` NO está en el repo
   - [ ] `.gitignore` está correcto
   - [ ] Usar `git log` para verificar que no hay secrets en historial

### 5. Para usuarios que clonen:
   - Deben copiar `.env.example` → `.env`
   - Deben completar sus propias credenciales
   - Deben instalar con `pip install -r requirements.txt`

---

## 🚀 CHECKLIST FINAL:

- [x] Credenciales removidas del código
- [x] Variables de entorno configuradas
- [x] `.env.example` creado
- [x] Debug mode desactivado
- [x] `.gitignore` contiene archivos sensibles
- [x] README actualizado con instrucciones de seguridad
- [x] HTTPS recomendado en producción
- [x] SQL Injection mitigado (usando parameterized queries)
- [x] XSS considerado (templates usan Jinja2 escaping)

---

## ⚠️ CONSIDERACIONES ADICIONALES:

### Para Producción:
1. Usar HTTPS obligatoriamente (no HTTP)
2. Configurar CORS si es necesario
3. Rate limiting en endpoints de login
4. Logging y monitoreo de intentos fallidos
5. SSL Certificate válido
6. Base de datos en servidor separado
7. Backups regulares

### Dependencias:
- Todas están en `requirements.txt`
- Google Auth validado desde servers de Google
- Bcrypt con salt automático (seguro)

---

## 🔗 REFERENCIAS:

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security](https://flask.palletsprojects.com/security/)
- [Google OAuth 2.0 Security](https://developers.google.com/identity/protocols/oauth2)
- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
