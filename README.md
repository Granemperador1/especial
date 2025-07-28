# MindSchool - Academia Digital

Una plataforma educativa moderna construida con Flask que permite a estudiantes e instructores gestionar cursos y aprendizaje en línea.

## 🚀 Características

- **Sistema de Autenticación**: Registro e inicio de sesión de usuarios
- **Gestión de Cursos**: Creación y administración de cursos
- **Sistema de Inscripciones**: Los estudiantes pueden inscribirse en cursos
- **Dashboard Personalizado**: Diferentes vistas para estudiantes e instructores
- **Interfaz Moderna**: Diseño responsive y atractivo

## 🛠️ Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos**: SQLite con SQLAlchemy
- **Autenticación**: Flask-Login
- **Frontend**: HTML, CSS, JavaScript
- **Formularios**: Flask-WTF

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/Granemperador1/especial.git
   cd especial
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar la aplicación**
   ```bash
   python app.py
   ```

5. **Abrir en el navegador**
   ```
   http://localhost:5000
   ```

## 📁 Estructura del Proyecto

```
especial/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Este archivo
├── templates/            # Plantillas HTML
│   └── index.html        # Página principal
├── uploads/              # Archivos subidos
└── venv/                 # Entorno virtual (no incluido en Git)
```

## 🗄️ Base de Datos

La aplicación utiliza SQLite con los siguientes modelos:

- **User**: Usuarios (estudiantes e instructores)
- **Course**: Cursos disponibles
- **Enrollment**: Inscripciones de estudiantes a cursos

## 🔐 Funcionalidades

### Para Estudiantes
- Registro e inicio de sesión
- Explorar cursos disponibles
- Inscribirse en cursos
- Ver dashboard personal

### Para Instructores
- Crear y gestionar cursos
- Ver estudiantes inscritos
- Dashboard de instructor

## 🚀 Despliegue

Para desplegar en producción:

1. Configurar variables de entorno
2. Usar un servidor WSGI como Gunicorn
3. Configurar una base de datos PostgreSQL
4. Configurar un servidor web como Nginx

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👨‍💻 Autor

**Granemperador1**
- GitHub: [@Granemperador1](https://github.com/Granemperador1)

## 🙏 Agradecimientos

- Flask y su comunidad
- Bootstrap para el diseño
- Todos los contribuidores del proyecto 