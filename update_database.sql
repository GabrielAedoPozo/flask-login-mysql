-- Script SQL para agregar columnas necesarias para Google OAuth
-- Ejecuta este script en tu base de datos login_db

USE login_db;

-- Agregar columnas para OAuth si no existen
ALTER TABLE users_new 
ADD COLUMN IF NOT EXISTS google_id VARCHAR(255) DEFAULT NULL,
ADD COLUMN IF NOT EXISTS picture VARCHAR(500) DEFAULT NULL,
ADD COLUMN IF NOT EXISTS auth_provider ENUM('local', 'google') DEFAULT 'local';

-- Crear índice en google_id para búsquedas rápidas
CREATE INDEX IF NOT EXISTS idx_google_id ON users_new(google_id);

-- Modificar columna password para permitir NULL (usuarios de Google no necesitan password)
ALTER TABLE users_new MODIFY password VARCHAR(255) DEFAULT NULL;

-- Mostrar estructura actualizada
DESCRIBE users_new;
