#!/bin/sh

# Générer le certificat SSL si il n'existe pas
if [ ! -f "/etc/nginx/ssl/nginx.crt" ]; then
    echo "Génération du certificat SSL..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout /etc/nginx/ssl/nginx.key \
        -out /etc/nginx/ssl/nginx.crt \
        -subj "/C=FR/ST=IDF/L=Paris/O=42/OU=42/CN=${DOMAIN_NAME}"
    
    echo "Certificat SSL généré avec succès !"
fi

# Remplacer ${DOMAIN_NAME} dans la config Nginx
echo "Configuration de Nginx pour ${DOMAIN_NAME}..."
envsubst '${DOMAIN_NAME}' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf

echo "Démarrage de Nginx..."
# Démarrer Nginx en foreground (pas de daemon)
exec nginx -g "daemon off;"
