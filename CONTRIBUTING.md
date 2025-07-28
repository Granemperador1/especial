# Contribuir a MindSchool

¡Gracias por tu interés en contribuir a MindSchool! Este documento te guiará a través del proceso de contribución.

## 🚀 Cómo Contribuir

### 1. Fork del Repositorio
1. Ve a [GitHub](https://github.com/tu-usuario/mindschool)
2. Haz clic en "Fork" en la esquina superior derecha
3. Clona tu fork localmente:
   ```bash
   git clone https://github.com/tu-usuario/mindschool.git
   cd mindschool
   ```

### 2. Configurar el Entorno de Desarrollo
1. Crear entorno virtual:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configurar base de datos:
   - Instalar PostgreSQL
   - Crear base de datos `mindschool`
   - Configurar variables en `config.py`

### 3. Crear una Rama
```bash
git checkout -b feature/nueva-funcionalidad
```

### 4. Hacer Cambios
- Escribe código limpio y bien documentado
- Sigue las convenciones de Python (PEP 8)
- Agrega tests para nuevas funcionalidades
- Actualiza la documentación si es necesario

### 5. Ejecutar Tests
```bash
python3 run_tests.py
```

### 6. Commit y Push
```bash
git add .
git commit -m "feat: agregar nueva funcionalidad"
git push origin feature/nueva-funcionalidad
```

### 7. Crear Pull Request
1. Ve a tu fork en GitHub
2. Haz clic en "New Pull Request"
3. Selecciona tu rama
4. Describe tus cambios
5. Envía el PR

## 📋 Guías de Desarrollo

### Estructura del Proyecto
```
mindschool/
├── app.py              # Aplicación principal Flask
├── config.py           # Configuración de la base de datos
├── templates/          # Plantillas HTML
├── uploads/           # Archivos subidos
├── tests/             # Tests del proyecto
├── requirements.txt   # Dependencias Python
└── README.md         # Documentación
```

### Convenciones de Código
- **Python:** PEP 8
- **HTML/CSS:** Indentación de 2 espacios
- **JavaScript:** ES6+ con semicolons
- **Commits:** Conventional Commits
- **Branches:** feature/, bugfix/, hotfix/

### Tests
- Escribe tests para todas las nuevas funcionalidades
- Mantén cobertura de código > 80%
- Ejecuta tests antes de cada commit

## 🐛 Reportar Bugs

1. Usa el template de issue de GitHub
2. Incluye pasos para reproducir el bug
3. Describe el comportamiento esperado vs actual
4. Adjunta logs y screenshots si es relevante

## 💡 Solicitar Funcionalidades

1. Verifica que la funcionalidad no exista ya
2. Describe el caso de uso
3. Explica el beneficio para los usuarios
4. Proporciona ejemplos si es posible

## 📝 Documentación

- Mantén el README actualizado
- Documenta nuevas APIs
- Agrega ejemplos de uso
- Incluye screenshots para cambios de UI

## 🤝 Código de Conducta

- Sé respetuoso y inclusivo
- Ayuda a otros contribuyentes
- Mantén discusiones constructivas
- Respeta las decisiones del equipo

## 🏷️ Etiquetas de Issues

- `bug` - Error en el código
- `enhancement` - Nueva funcionalidad
- `documentation` - Mejoras en documentación
- `good first issue` - Ideal para principiantes
- `help wanted` - Necesita ayuda
- `question` - Pregunta general

## 📞 Contacto

- **Issues:** [GitHub Issues](https://github.com/tu-usuario/mindschool/issues)
- **Discussions:** [GitHub Discussions](https://github.com/tu-usuario/mindschool/discussions)

¡Gracias por contribuir a hacer MindSchool mejor! 🎓 