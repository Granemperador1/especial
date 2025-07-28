# Despliegue en Railway - Paso a Paso

## 🚀 Railway es GRATUITO y perfecto para Flask

### Paso 1: Crear cuenta en Railway
1. Ve a [railway.app](https://railway.app)
2. Haz clic en "Start a New Project"
3. Selecciona "Deploy from GitHub repo"
4. Conecta tu cuenta de GitHub

### Paso 2: Conectar tu repositorio
1. Busca tu repositorio: `Granemperador1/especial`
2. Haz clic en "Deploy Now"
3. Railway detectará automáticamente que es Python

### Paso 3: Configurar variables (opcional)
En Railway, ve a la pestaña "Variables":
```
FLASK_ENV=production
SECRET_KEY=tu-clave-secreta-muy-segura
```

### Paso 4: Obtener tu URL
- Railway te dará una URL como: `https://tu-app.railway.app`
- Tu aplicación estará funcionando en 2-3 minutos

### Paso 5: Conectar tu dominio
1. En Railway, ve a "Settings" > "Domains"
2. Agrega tu dominio: `mindschoo.store`
3. Railway te dará instrucciones para configurar DNS

## 🔧 Configurar DNS en Hostinger

1. Ve a tu panel de Hostinger: https://hpanel.hostinger.com
2. Ve a "Dominios" > "mindschoo.store" > "DNS"
3. Agrega estos registros:
   - **Tipo**: CNAME
   - **Nombre**: @
   - **Valor**: `tu-app.railway.app`
   - **TTL**: 300

## ✅ Ventajas de Railway
- ✅ Completamente GRATUITO
- ✅ Despliegue automático desde GitHub
- ✅ SSL automático
- ✅ Soporte para Python/Flask
- ✅ Muy fácil de usar
- ✅ Sin configuración compleja 