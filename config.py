import os

# Configuración de la base de datos PostgreSQL
class DatabaseConfig:
    HOST = os.getenv('DB_HOST', 'localhost')
    DATABASE = os.getenv('DB_NAME', 'mindschool')
    USER = os.getenv('DB_USER', 'postgres')
    PASSWORD = os.getenv('DB_PASSWORD', '123456')
    PORT = os.getenv('DB_PORT', '5432')
    
    @classmethod
    def get_config(cls):
        """Retorna la configuración como diccionario"""
        return {
            'host': cls.HOST,
            'database': cls.DATABASE,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'port': cls.PORT
        }

# Configuración de la aplicación Flask
class AppConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'tu_clave_secreta_aqui')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

# Configuración de seguridad
class SecurityConfig:
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hora 