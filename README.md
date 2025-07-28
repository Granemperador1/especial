# MindSchool - Academia Digital

Sistema de gestión educativa con interfaz web moderna y base de datos PostgreSQL.

## Características

- 🔐 **Autenticación de usuarios** (Estudiantes, Profesores, Administradores)
- 💳 **Sistema de pagos** en línea
- 💬 **Foro académico** para discusiones
- ✉️ **Sistema de mensajería** interno
- 📚 **Gestión de tareas** y asignaciones
- 🎥 **Biblioteca de videos** educativos
- 🎨 **Interfaz moderna** y responsiva

## Estructura del Proyecto

```
base_de_datos/
├── app.py              # Aplicación Flask principal
├── config.py           # Configuración de la base de datos
├── index.html          # Interfaz HTML
├── requirements.txt    # Dependencias Python
├── README.md          # Este archivo
└── uploads/           # Carpeta para archivos subidos
```

## Instalación

### 1. Requisitos Previos

- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)

### 2. Configuración de la Base de Datos

1. **Instalar PostgreSQL:**
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install postgresql postgresql-contrib
   
   # CentOS/RHEL
   sudo yum install postgresql postgresql-server
   ```

2. **Crear la base de datos:**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE mindschool;
   CREATE USER mindschool_user WITH PASSWORD 'tu_password';
   GRANT ALL PRIVILEGES ON DATABASE mindschool TO mindschool_user;
   \q
   ```

### 3. Configuración del Proyecto

1. **Clonar o descargar el proyecto:**
   ```bash
   cd /ruta/del/proyecto
   ```

2. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno:**
   Crear un archivo `.env` en la raíz del proyecto:
   ```env
   DB_HOST=localhost
   DB_NAME=mindschool
   DB_USER=mindschool_user
   DB_PASSWORD=tu_password
   DB_PORT=5432
   SECRET_KEY=tu_clave_secreta_muy_segura
   DEBUG=True
   ```

4. **Crear carpeta de uploads:**
   ```bash
   mkdir uploads
   ```

### 4. Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5000`

## Uso

### Usuarios de Prueba

La aplicación incluye usuarios de ejemplo:

- **Estudiante:** estudiante@mindschool.com / password123
- **Profesor:** profesor@mindschool.com / password123
- **Administrador:** admin@mindschool.com / password123

### Funcionalidades

1. **Inicio de Sesión:** Accede con tu tipo de usuario y credenciales
2. **Pagos:** Realiza pagos de matrícula y servicios
3. **Foro:** Participa en discusiones académicas
4. **Mensajes:** Comunícate con profesores y compañeros
5. **Tareas:** Sube y gestiona tus tareas académicas
6. **Videos:** Accede a contenido multimedia educativo

## Conexión a PostgreSQL

### Ubicación de la Conexión

La conexión a PostgreSQL se encuentra en:

- **Archivo:** `app.py`
- **Función:** `get_db_connection()` (línea ~20)
- **Configuración:** `config.py`

### Configuración de la Conexión

```python
# En config.py
DB_CONFIG = {
    'host': 'localhost',      # Servidor PostgreSQL
    'database': 'mindschool', # Nombre de la base de datos
    'user': 'postgres',       # Usuario de la base de datos
    'password': 'password',   # Contraseña del usuario
    'port': '5432'           # Puerto de PostgreSQL
}
```

### Inicialización de la Base de Datos

La aplicación crea automáticamente las tablas necesarias:

- `users` - Usuarios del sistema
- `courses` - Cursos disponibles
- `assignments` - Tareas y asignaciones
- `payments` - Registro de pagos
- `forum_posts` - Posts del foro
- `messages` - Mensajes internos
- `videos` - Biblioteca de videos

## Desarrollo

### Estructura de la Base de Datos

```sql
-- Ejemplo de consultas útiles
SELECT * FROM users WHERE user_type = 'student';
SELECT * FROM assignments WHERE student_id = 1;
SELECT * FROM forum_posts ORDER BY created_at DESC;
```

### API Endpoints

- `POST /login` - Autenticación
- `POST /payment` - Procesar pagos
- `POST /forum/post` - Crear post
- `GET /forum/posts` - Obtener posts
- `POST /message/send` - Enviar mensaje
- `GET /messages/<user_id>` - Obtener mensajes
- `POST /task/upload` - Subir tarea
- `GET /tasks/<user_id>` - Obtener tareas
- `GET /videos` - Obtener videos

## Seguridad

- Contraseñas hasheadas con Werkzeug
- Validación de formularios
- Protección CSRF
- Configuración segura de cookies
- Límites de tamaño de archivo

## Solución de Problemas

### Error de Conexión a PostgreSQL

1. Verificar que PostgreSQL esté ejecutándose:
   ```bash
   sudo systemctl status postgresql
   ```

2. Verificar credenciales en `config.py`

3. Probar conexión manual:
   ```bash
   psql -h localhost -U postgres -d mindschool
   ```

### Error de Permisos

1. Verificar permisos de la carpeta `uploads`:
   ```bash
   chmod 755 uploads
   ```

2. Verificar permisos del usuario de la base de datos

## Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. 