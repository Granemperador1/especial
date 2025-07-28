# Despliegue en Hostinger - Hosting Compartido

## ⚠️ Limitaciones del Hosting Compartido

El hosting compartido de Hostinger tiene limitaciones para aplicaciones Flask:
- No permite ejecutar procesos en segundo plano
- No tiene acceso SSH completo
- Limitaciones de Python

## 🔄 Alternativas Recomendadas

### Opción 1: Migrar a VPS de Hostinger
1. Ve a tu panel de Hostinger
2. Actualiza tu plan a VPS
3. Sigue las instrucciones del archivo `deploy_hostinger.sh`

### Opción 2: Usar Hostinger Cloud
1. Accede a tu panel de Hostinger
2. Ve a "Cloud Hosting"
3. Crea un nuevo proyecto
4. Conecta tu repositorio de GitHub

### Opción 3: Plataformas Gratuitas
- **Railway**: railway.app
- **Render**: render.com
- **Vercel**: vercel.com
- **Heroku**: heroku.com

## 📋 Pasos para VPS de Hostinger

1. **Accede a tu VPS via SSH**
   ```bash
   ssh root@tu-ip-del-vps
   ```

2. **Ejecuta el script de despliegue**
   ```bash
   chmod +x deploy_hostinger.sh
   ./deploy_hostinger.sh
   ```

3. **Configura tu dominio**
   - Ve al panel de Hostinger
   - Configura los DNS para apuntar a tu VPS
   - Actualiza el archivo de Nginx con tu dominio real

4. **Configura SSL**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d tu-dominio.com
   ```

## 🔧 Configuración Manual (VPS)

Si prefieres hacerlo manualmente:

1. **Instalar dependencias**
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip python3-venv nginx git
   ```

2. **Clonar el proyecto**
   ```bash
   cd /var/www
   sudo git clone https://github.com/Granemperador1/especial.git mindschool
   sudo chown -R $USER:$USER mindschool
   cd mindschool
   ```

3. **Configurar entorno virtual**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configurar Gunicorn**
   ```bash
   gunicorn --bind 127.0.0.1:8000 wsgi:app
   ```

5. **Configurar Nginx** (ver archivo de configuración en el script)

## 📞 Soporte

Si necesitas ayuda:
1. Contacta al soporte de Hostinger
2. Solicita migración a VPS
3. Pide asistencia para configuración de Python 