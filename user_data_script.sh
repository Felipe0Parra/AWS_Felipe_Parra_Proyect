# --- FASE 1: Configuración Inicial (User Data) ---
# (Esto ya se ejecutó al crear la instancia, pero es parte del registro)
#!/bin/bash
apt-get update -y
apt-get install -y nginx unzip
systemctl start nginx
systemctl enable nginx
echo "<h1>Proyecto 18: Observabilidad Activa</h1>" > /var/www/html/index.html

# Instalación de Agentes AWS
cd /tmp
wget https://s3.us-east-2.amazonaws.com/aws-xray-assets.us-east-2/xray-daemon/aws-xray-daemon-3.x.deb
dpkg -i aws-xray-daemon-3.x.deb
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
dpkg -i -E ./amazon-cloudwatch-agent.deb


# --- FASE 2: Configuración del CloudWatch Agent ---
# Ejecutar el asistente
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
# Arrancar el agente con la config
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl -a fetch-config -m ec2 -s -c file:/opt/aws/amazon-cloudwatch-agent/bin/config.json


# --- FASE 4: Instalación de Grafana (Manual) ---
# Descargar el binario directamente (versión compatible)
cd /tmp
wget https://dl.grafana.com/oss/release/grafana_10.0.3_amd64.deb

# Instalar
sudo dpkg -i grafana_10.0.3_amd64.deb

# Iniciar el servicio
sudo systemctl daemon-reload
sudo systemctl start grafana-server
sudo systemctl enable grafana-server

# Instalación del Plugin de X-Ray (Adicional)
sudo grafana-cli plugins install grafana-x-ray-datasource
sudo systemctl restart grafana-server


# --- GENERACIÓN DE TRÁFICO (Pruebas de Carga) ---
# Instalación de Apache Bench
sudo apt-get install -y apache2-utils

# Lanzar carga masiva (5000 peticiones, 10 concurrentes)
ab -n 5000 -c 10 http://localhost/
