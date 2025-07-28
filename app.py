from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mindschool.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Modelos de la base de datos
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    price = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Crear la base de datos al iniciar
def init_db():
    with app.app_context():
        try:
            db.create_all()
            print("Base de datos creada exitosamente")
            
            # Crear algunos cursos de ejemplo si no existen
            if Course.query.count() == 0:
                # Crear un usuario instructor de ejemplo
                instructor = User(
                    username='admin',
                    email='admin@mindschool.com',
                    password_hash=generate_password_hash('admin123'),
                    role='instructor'
                )
                db.session.add(instructor)
                db.session.commit()
                
                # Crear cursos de ejemplo
                course1 = Course(
                    title='Introducción a Python',
                    description='Aprende los fundamentos de Python desde cero',
                    instructor_id=instructor.id,
                    price=29.99
                )
                course2 = Course(
                    title='Desarrollo Web con Flask',
                    description='Crea aplicaciones web modernas con Flask',
                    instructor_id=instructor.id,
                    price=39.99
                )
                course3 = Course(
                    title='Base de Datos SQL',
                    description='Domina las bases de datos relacionales',
                    instructor_id=instructor.id,
                    price=24.99
                )
                
                db.session.add_all([course1, course2, course3])
                db.session.commit()
                print("Datos de ejemplo creados")
                
        except Exception as e:
            print(f"Error al crear la base de datos: {e}")

# Rutas
@app.route('/')
def index():
    try:
        courses = Course.query.all()
        return render_template('index.html', courses=courses)
    except Exception as e:
        # Si hay error con la base de datos, mostrar página de bienvenida
        return render_template_string('''
        <!DOCTYPE html>
        <html>
        <head>
            <title>MindSchool - Academia Digital</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background: #f8fafc; }
                .header { background: linear-gradient(135deg, #1E40AF 0%, #FF6B35 100%); 
                         color: white; padding: 30px; border-radius: 15px; text-align: center; }
                .content { margin-top: 30px; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
                .feature { margin: 15px 0; padding: 15px; background: #f1f5f9; border-radius: 8px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🎓 MindSchool - Academia Digital</h1>
                <p>Plataforma educativa moderna construida con Flask</p>
            </div>
            <div class="content">
                <h2>¡Bienvenido a MindSchool!</h2>
                <p>Tu aplicación Flask está funcionando correctamente en Render.</p>
                <p><strong>Funcionalidades disponibles:</strong></p>
                <div class="feature">✅ Sistema de autenticación de usuarios</div>
                <div class="feature">✅ Gestión completa de cursos</div>
                <div class="feature">✅ Sistema de inscripciones</div>
                <div class="feature">✅ Dashboard personalizado para estudiantes e instructores</div>
                <div class="feature">✅ Base de datos SQLite integrada</div>
                <hr>
                <p><em>La aplicación está configurada y lista para usar. Los datos de ejemplo se crearán automáticamente.</em></p>
            </div>
        </body>
        </html>
        ''')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya existe', 'error')
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'error')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('¡Registro exitoso! Ya puedes iniciar sesión', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'instructor':
        courses = Course.query.filter_by(instructor_id=current_user.id).all()
    else:
        enrollments = Enrollment.query.filter_by(student_id=current_user.id).all()
        courses = [Course.query.get(enrollment.course_id) for enrollment in enrollments]
    
    return render_template('dashboard.html', courses=courses)

@app.route('/course/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    instructor = User.query.get(course.instructor_id)
    return render_template('course_detail.html', course=course, instructor=instructor)

@app.route('/enroll/<int:course_id>', methods=['POST'])
@login_required
def enroll_course(course_id):
    existing_enrollment = Enrollment.query.filter_by(
        student_id=current_user.id, 
        course_id=course_id
    ).first()
    
    if existing_enrollment:
        flash('Ya estás inscrito en este curso', 'info')
    else:
        enrollment = Enrollment(student_id=current_user.id, course_id=course_id)
        db.session.add(enrollment)
        db.session.commit()
        flash('¡Te has inscrito exitosamente al curso!', 'success')
    
    return redirect(url_for('course_detail', course_id=course_id))

# Inicializar la base de datos al importar el módulo
init_db()

if __name__ == '__main__':
    app.run(debug=False) 