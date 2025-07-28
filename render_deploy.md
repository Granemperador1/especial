# Despliegue en Render - Paso a Paso

## 🚀 Render es GRATUITO y confiable

### Paso 1: Crear cuenta en Render
1. Ve a [render.com](https://render.com)
2. Haz clic en "Get Started"
3. Conecta tu cuenta de GitHub

### Paso 2: Crear nuevo servicio
1. Haz clic en "New +"
2. Selecciona "Web Service"
3. Conecta tu repositorio: `Granemperador1/especial`

### Paso 3: Configurar el servicio
- **Name**: mindschool
- **Environment**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn wsgi:app`

### Paso 4: Desplegar
1. Haz clic en "Create Web Service"
2. Render comenzará el despliegue automáticamente
3. En 5-10 minutos tu app estará lista

### Paso 5: Conectar dominio
1. En tu servicio, ve a "Settings" > "Custom Domains"
2. Agrega: `mindschoo.store`
3. Render te dará instrucciones de DNS

## 🔧 Configurar DNS en Hostinger

1. Ve a tu panel de Hostinger
2. Dominios > mindschoo.store > DNS
3. Agrega:
   - **Tipo**: CNAME
   - **Nombre**: @
   - **Valor**: `tu-app.onrender.com`
   - **TTL**: 300

## ✅ Ventajas de Render
- ✅ Plan gratuito generoso
- ✅ Despliegue automático
- ✅ SSL automático
- ✅ Muy confiable
- ✅ Soporte técnico 