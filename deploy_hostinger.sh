#!/bin/bash
echo "=== Despliegue en Hostinger VPS ==="

# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python y pip
sudo apt install python3 python3-pip python3-venv nginx -y

# Instalar supervisor para gestionar el proceso
sudo apt install supervisor -y

# Crear directorio para la aplicación
sudo mkdir -p /var/www/mindschool
sudo chown $USER:$USER /var/www/mindschool

# Clonar el repositorio
cd /var/www/mindschool
git clone https://github.com/Granemperador1/especial.git .

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Crear directorio de uploads
mkdir -p uploads

# Configurar la aplicación
echo "Configurando la aplicación..."

# Crear archivo de configuración de supervisor
sudo tee /etc/supervisor/conf.d/mindschool.conf > /dev/null <<EOF
[program:mindschool]
directory=/var/www/mindschool
command=/var/www/mindschool/venv/bin/gunicorn --bind 127.0.0.1:8000 wsgi:app
autostart=true
autorestart=true
stderr_logfile=/var/log/mindschool.err.log
stdout_logfile=/var/log/mindschool.out.log
user=$USER
EOF

# Configurar Nginx
sudo tee /etc/nginx/sites-available/mindschool > /dev/null <<EOF
server {
    listen 80;
    server_name tu-dominio.com www.tu-dominio.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /static {
        alias /var/www/mindschool/static;
    }
}
EOF

# Habilitar el sitio
sudo ln -s /etc/nginx/sites-available/mindschool /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Reiniciar servicios
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start mindschool
sudo systemctl restart nginx

echo "=== Despliegue completado ==="
echo "Tu aplicación estará disponible en: http://tu-dominio.com" 