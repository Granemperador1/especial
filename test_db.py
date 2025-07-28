#!/usr/bin/env python3
"""
Script para probar la conexión a PostgreSQL
"""

import psycopg2
import sys
from config import DatabaseConfig

def test_postgresql_connection():
    """Probar conexión a PostgreSQL"""
    print("🔗 PROBANDO CONEXIÓN A POSTGRESQL")
    print("="*50)
    
    # Obtener configuración
    config = DatabaseConfig.get_config()
    print(f"📋 Configuración:")
    print(f"   Host: {config['host']}")
    print(f"   Database: {config['database']}")
    print(f"   User: {config['user']}")
    print(f"   Port: {config['port']}")
    print(f"   Password: {'*' * len(config['password'])}")
    
    try:
        # Intentar conexión
        print(f"\n🔌 Conectando a PostgreSQL...")
        conn = psycopg2.connect(**config)
        
        # Verificar conexión
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ Conexión exitosa!")
        print(f"📊 Versión de PostgreSQL: {version[0]}")
        
        # Verificar si la base de datos existe
        cursor.execute("SELECT current_database();")
        current_db = cursor.fetchone()
        print(f"🗄️  Base de datos actual: {current_db[0]}")
        
        # Verificar tablas existentes
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        print(f"\n📋 Tablas existentes:")
        if tables:
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("   No hay tablas en la base de datos")
        
        # Cerrar conexión
        cursor.close()
        conn.close()
        
        print(f"\n🎉 ¡Conexión a PostgreSQL funcionando correctamente!")
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Error de conexión: {e}")
        print(f"\n💡 Posibles soluciones:")
        print(f"   1. Verificar que PostgreSQL esté ejecutándose")
        print(f"   2. Verificar credenciales en config.py")
        print(f"   3. Verificar que la base de datos 'mindschool' exista")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_database_creation():
    """Probar creación de base de datos"""
    print(f"\n🔧 PROBANDO CREACIÓN DE BASE DE DATOS")
    print("="*50)
    
    config = DatabaseConfig.get_config()
    
    try:
        # Conectar a postgres (base de datos por defecto)
        config_temp = config.copy()
        config_temp['database'] = 'postgres'
        conn = psycopg2.connect(**config_temp)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Verificar si la base de datos existe
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s;", (config['database'],))
        exists = cursor.fetchone()
        
        if exists:
            print(f"✅ La base de datos '{config['database']}' ya existe")
        else:
            print(f"📝 Creando base de datos '{config['database']}'...")
            cursor.execute(f"CREATE DATABASE {config['database']};")
            print(f"✅ Base de datos '{config['database']}' creada exitosamente")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def test_table_creation():
    """Probar creación de tablas"""
    print(f"\n📋 PROBANDO CREACIÓN DE TABLAS")
    print("="*50)
    
    from app import init_database
    
    try:
        success = init_database()
        if success:
            print("✅ Tablas creadas/verificadas exitosamente")
            return True
        else:
            print("❌ Error creando tablas")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Función principal"""
    print("🎓 MINDSCHOOL - PRUEBA DE BASE DE DATOS")
    print("="*60)
    
    # Test 1: Conexión básica
    if not test_postgresql_connection():
        print(f"\n❌ No se pudo conectar a PostgreSQL")
        print(f"💡 Asegúrate de que PostgreSQL esté instalado y ejecutándose")
        sys.exit(1)
    
    # Test 2: Creación de base de datos
    if not test_database_creation():
        print(f"\n❌ No se pudo crear la base de datos")
        sys.exit(1)
    
    # Test 3: Creación de tablas
    if not test_table_creation():
        print(f"\n❌ No se pudieron crear las tablas")
        sys.exit(1)
    
    print(f"\n🎉 ¡TODAS LAS PRUEBAS DE BASE DE DATOS PASARON!")
    print(f"🚀 La aplicación está lista para ejecutarse")

if __name__ == "__main__":
    main() 