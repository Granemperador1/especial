from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import json
from config import DatabaseConfig, AppConfig, SecurityConfig

app = Flask(__name__)
app.secret_key = AppConfig.SECRET_KEY

# Configuración de la base de datos PostgreSQL
DB_CONFIG = DatabaseConfig.get_config()

def get_db_connection():
    """Establece conexión con la base de datos PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        conn.autocommit = False
        return conn
    except psycopg2.Error as e:
        print(f"Error conectando a PostgreSQL: {e}")
        return None

def init_database():
    """Inicializa las tablas de la base de datos"""
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        # Crear tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                name VARCHAR(255) NOT NULL,
                user_type VARCHAR(50) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear tabla de cursos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS courses (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                teacher_id INTEGER REFERENCES users(id),
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear tabla de tareas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS assignments (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                subject VARCHAR(100) NOT NULL,
                description TEXT,
                file_path VARCHAR(500),
                student_id INTEGER REFERENCES users(id),
                status VARCHAR(50) DEFAULT 'pending',
                grade DECIMAL(5,2),
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear tabla de pagos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id),
                payment_type VARCHAR(100) NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                status VARCHAR(50) DEFAULT 'pending',
                transaction_id VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear tabla de posts del foro
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS forum_posts (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                category VARCHAR(100) NOT NULL,
                author_id INTEGER REFERENCES users(id),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear tabla de mensajes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id SERIAL PRIMARY KEY,
                sender_id INTEGER REFERENCES users(id),
                recipient_id INTEGER REFERENCES users(id),
                subject VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                read BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Crear tabla de videos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                subject VARCHAR(100) NOT NULL,
                duration INTEGER,
                difficulty VARCHAR(50),
                video_url VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Insertar datos de ejemplo si no existen
        cursor.execute("SELECT COUNT(*) FROM users")
        if cursor.fetchone()[0] == 0:
            # Insertar usuarios de ejemplo
            users_data = [
                ('estudiante@mindschool.com', 'password123', 'Juan Pérez', 'student'),
                ('profesor@mindschool.com', 'password123', 'María González', 'teacher'),
                ('admin@mindschool.com', 'password123', 'Carlos Admin', 'admin')
            ]
            
            for email, password, name, user_type in users_data:
                password_hash = generate_password_hash(password)
                cursor.execute("""
                    INSERT INTO users (email, password_hash, name, user_type)
                    VALUES (%s, %s, %s, %s)
                """, (email, password_hash, name, user_type))
            
            # Insertar cursos de ejemplo
            cursor.execute("""
                INSERT INTO courses (name, teacher_id, description)
                VALUES 
                ('Matemáticas', 2, 'Curso de matemáticas básicas'),
                ('Español', 2, 'Curso de literatura y gramática'),
                ('Ciencias', 2, 'Curso de ciencias naturales')
            """)
            
            # Insertar videos de ejemplo
            videos_data = [
                ('Introducción al Álgebra', 'Conceptos básicos del álgebra', 'Matemáticas', 45, 'Básico'),
                ('Historia de México', 'Historia de México desde la independencia', 'Historia', 80, 'Intermedio'),
                ('Experimentos de Física', 'Experimentos prácticos de física', 'Ciencias', 35, 'Avanzado'),
                ('Literatura Contemporánea', 'Análisis de obras literarias modernas', 'Español', 55, 'Básico'),
                ('English Grammar', 'Gramática inglesa básica', 'Inglés', 40, 'Intermedio'),
                ('Geografía Mundial', 'Geografía física y política mundial', 'Geografía', 70, 'Avanzado')
            ]
            
            for title, description, subject, duration, difficulty in videos_data:
                cursor.execute("""
                    INSERT INTO videos (title, description, subject, duration, difficulty)
                    VALUES (%s, %s, %s, %s, %s)
                """, (title, description, subject, duration, difficulty))
        
        conn.commit()
        print("Base de datos inicializada correctamente")
        return True
        
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error inicializando base de datos: {e}")
        return False
    finally:
        conn.close()

# Rutas de la aplicación

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    """Autenticación de usuarios"""
    try:
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['userType']
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Buscar usuario
        cursor.execute("""
            SELECT id, email, password_hash, name, user_type 
            FROM users 
            WHERE email = %s AND user_type = %s
        """, (email, user_type))
        
        user = cursor.fetchone()
        
        if user and check_password_hash(user['password_hash'], password):
            # Usuario autenticado correctamente
            return jsonify({
                'success': True,
                'user': {
                    'id': user['id'],
                    'name': user['name'],
                    'email': user['email'],
                    'type': user['user_type']
                }
            })
        else:
            return jsonify({'error': 'Credenciales incorrectas'}), 401
            
    except Exception as e:
        print(f"Error en login: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500
    finally:
        if conn:
            conn.close()

@app.route('/payment', methods=['POST'])
def process_payment():
    """Procesar pagos"""
    try:
        user_id = request.form.get('user_id')
        payment_type = request.form['paymentType']
        amount = request.form['amount']
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
        cursor = conn.cursor()
        
        # Insertar pago
        cursor.execute("""
            INSERT INTO payments (user_id, payment_type, amount, status, transaction_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, payment_type, amount, 'completed', f"TXN_{datetime.now().strftime('%Y%m%d%H%M%S')}"))
        
        conn.commit()
        
        return jsonify({'success': True, 'message': 'Pago procesado exitosamente'})
        
    except Exception as e:
        print(f"Error procesando pago: {e}")
        return jsonify({'error': 'Error procesando el pago'}), 500
    finally:
        if conn:
            conn.close()

@app.route('/forum/post', methods=['POST'])
def create_forum_post():
    """Crear nuevo post en el foro"""
    try:
        title = request.form['title']
        category = request.form['category']
        content = request.form['content']
        author_id = request.form.get('author_id')
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO forum_posts (title, content, category, author_id)
            VALUES (%s, %s, %s, %s)
        """, (title, content, category, author_id))
        
        conn.commit()
        
        return jsonify({'success': True, 'message': 'Post creado exitosamente'})
        
    except Exception as e:
        print(f"Error creando post: {e}")
        return jsonify({'error': 'Error creando el post'}), 500
    finally:
        if conn:
            conn.close()

@app.route('/forum/posts')
def get_forum_posts():
    """Obtener posts del foro"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cursor.execute("""
            SELECT fp.*, u.name as author_name
            FROM forum_posts fp
            JOIN users u ON fp.author_id = u.id
            ORDER BY fp.created_at DESC
        """)
        
        posts = cursor.fetchall()
        
        return jsonify({'posts': posts})
        
    except Exception as e:
        print(f"Error obteniendo posts: {e}")
        return jsonify({'error': 'Error obteniendo posts'}), 500
    finally:
        if conn:
            conn.close()

@app.route('/message/send', methods=['POST'])
def send_message():
    """Enviar mensaje"""
    try:
        sender_id = request.form.get('sender_id')
        recipient_id = request.form['recipient']
        subject = request.form['subject']
        content = request.form['content']
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO messages (sender_id, recipient_id, subject, content)
            VALUES (%s, %s, %s, %s)
        """, (sender_id, recipient_id, subject, content))
        
        conn.commit()
        
        return jsonify({'success': True, 'message': 'Mensaje enviado exitosamente'})
        
    except Exception as e:
        print(f"Error enviando mensaje: {e}")
        return jsonify({'error': 'Error enviando mensaje'}), 500
    finally:
        if conn:
            conn.close()

@app.route('/messages/<int:user_id>')
def get_messages(user_id):
    """Obtener mensajes de un usuario"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cursor.execute("""
            SELECT m.*, 
                   s.name as sender_name,
                   r.name as recipient_name
            FROM messages m
            JOIN users s ON m.sender_id = s.id
            JOIN users r ON m.recipient_id = r.id
            WHERE m.sender_id = %s OR m.recipient_id = %s
            ORDER BY m.created_at DESC
        """, (user_id, user_id))
        
        messages = cursor.fetchall()
        
        return jsonify({'messages': messages})
        
    except Exception as e:
        print(f"Error obteniendo mensajes: {e}")
        return jsonify({'error': 'Error obteniendo mensajes'}), 500
    finally:
        if conn:
            conn.close()

@app.route('/task/upload', methods=['POST'])
def upload_task():
    """Subir tarea"""
    try:
        title = request.form['title']
        subject = request.form['subject']
        description = request.form.get('description', '')
        student_id = request.form.get('student_id')
        
        # Manejo de archivos
        file = request.files.get('file')
        file_path = None
        
        if file:
            # Guardar archivo (en producción usar un servicio de almacenamiento)
            filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
            file_path = f"uploads/{filename}"
            file.save(file_path)
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO assignments (title, subject, description, file_path, student_id, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (title, subject, description, file_path, student_id, 'pending'))
        
        conn.commit()
        
        return jsonify({'success': True, 'message': 'Tarea subida exitosamente'})
        
    except Exception as e:
        print(f"Error subiendo tarea: {e}")
        return jsonify({'error': 'Error subiendo tarea'}), 500
    finally:
        if conn:
            conn.close()

@app.route('/tasks/<int:user_id>')
def get_tasks(user_id):
    """Obtener tareas de un usuario"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cursor.execute("""
            SELECT a.*, u.name as student_name
            FROM assignments a
            JOIN users u ON a.student_id = u.id
            WHERE a.student_id = %s
            ORDER BY a.submitted_at DESC
        """, (user_id,))
        
        tasks = cursor.fetchall()
        
        return jsonify({'tasks': tasks})
        
    except Exception as e:
        print(f"Error obteniendo tareas: {e}")
        return jsonify({'error': 'Error obteniendo tareas'}), 500
    finally:
        if conn:
            conn.close()

@app.route('/videos')
def get_videos():
    """Obtener videos"""
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Error de conexión a la base de datos'}), 500
        
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cursor.execute("""
            SELECT * FROM videos
            ORDER BY created_at DESC
        """)
        
        videos = cursor.fetchall()
        
        return jsonify({'videos': videos})
        
    except Exception as e:
        print(f"Error obteniendo videos: {e}")
        return jsonify({'error': 'Error obteniendo videos'}), 500
    finally:
        if conn:
            conn.close()

# Función para ejecutar consultas SQL personalizadas
def execute_query(query, params=None):
    """Ejecuta una consulta SQL personalizada"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, params or ())
        
        if query.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
        else:
            conn.commit()
            result = {'affected_rows': cursor.rowcount}
        
        return result
        
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error ejecutando query: {e}")
        return None
    finally:
        conn.close()

# Función para llamar procedimientos almacenados
def call_stored_procedure(procedure_name, params=None):
    """Llama un procedimiento almacenado"""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # Construir la llamada al procedimiento
        param_placeholders = ', '.join(['%s'] * len(params)) if params else ''
        call_query = f"CALL {procedure_name}({param_placeholders})"
        
        cursor.execute(call_query, params or ())
        conn.commit()
        
        return {'success': True}
        
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error llamando procedimiento {procedure_name}: {e}")
        return {'success': False, 'error': str(e)}
    finally:
        conn.close()

if __name__ == '__main__':
    # Inicializar base de datos
    if init_database():
        print("Aplicación iniciada correctamente")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("Error iniciando la aplicación")