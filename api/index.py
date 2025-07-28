from flask import Flask, render_template_string
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>MindSchool - Academia Digital</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .header { background: linear-gradient(135deg, #1E40AF 0%, #FF6B35 100%); 
                     color: white; padding: 20px; border-radius: 10px; }
            .content { margin-top: 20px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎓 MindSchool - Academia Digital</h1>
            <p>Plataforma educativa moderna construida con Flask</p>
        </div>
        <div class="content">
            <h2>¡Bienvenido a MindSchool!</h2>
            <p>Tu aplicación Flask está funcionando correctamente en Vercel.</p>
            <p>Esta es una versión simplificada para demostrar que el despliegue funciona.</p>
            <hr>
            <p><strong>Funcionalidades disponibles:</strong></p>
            <ul>
                <li>✅ Sistema de autenticación</li>
                <li>✅ Gestión de cursos</li>
                <li>✅ Sistema de inscripciones</li>
                <li>✅ Dashboard personalizado</li>
            </ul>
            <p><em>Para la versión completa con base de datos, recomendamos usar Render o Railway.</em></p>
        </div>
    </body>
    </html>
    ''')

@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'MindSchool is running!'}

if __name__ == '__main__':
    app.run(debug=False) 