#!/bin/sh

set -e

echo "=== Démarrage du setup WordPress ==="

# Chargement des secrets
if [ ! -f "/run/secrets/db_password" ]; then
    echo "ERREUR: Secret db_password introuvable!"
    exit 1
fi

if [ ! -f "/run/secrets/credentials" ]; then
    echo "ERREUR: Secret credentials introuvable!"
    exit 1
fi

DB_PASSWORD=$(cat /run/secrets/db_password)
WP_ADMIN_PASSWORD=$(head -n 1 /run/secrets/credentials)
WP_USER_PASSWORD=$(tail -n 1 /run/secrets/credentials)

# Attendre que MariaDB soit prêt
echo "Attente de la disponibilité de MariaDB sur ${MYSQL_HOST}:3306..."
MAX_TRIES=30
COUNT=0
until nc -z "${MYSQL_HOST}" 3306 || [ $COUNT -eq $MAX_TRIES ]; do
    COUNT=$((COUNT + 1))
    echo "Tentative $COUNT/$MAX_TRIES..."
    sleep 2
done

if [ $COUNT -eq $MAX_TRIES ]; then
    echo "ERREUR: Impossible de se connecter à MariaDB!"
    exit 1
fi

echo "MariaDB est prêt !"

# Se déplacer dans le répertoire WordPress
cd /var/www/html

# Télécharger WordPress si pas déjà fait
if [ ! -f "wp-config.php" ]; then
    echo "Téléchargement de WordPress..."
    wp core download --allow-root
    
    echo "Configuration de WordPress..."
    wp config create \
        --dbname="${MYSQL_DATABASE}" \
        --dbuser="${MYSQL_USER}" \
        --dbpass="${DB_PASSWORD}" \
        --dbhost="${MYSQL_HOST}" \
        --allow-root
    
    # Attendre un peu que la config soit prête
    sleep 2
    
    echo "Installation de WordPress..."
    wp core install \
        --url="https://${DOMAIN_NAME}" \
        --title="${WP_TITLE}" \
        --admin_user="${WP_ADMIN_USER}" \
        --admin_password="${WP_ADMIN_PASSWORD}" \
        --admin_email="${WP_ADMIN_EMAIL}" \
        --skip-email \
        --allow-root
    
    echo "Création de l'utilisateur éditeur..."
    wp user create "${WP_USER}" "${WP_USER_EMAIL}" \
        --role=editor \
        --user_pass="${WP_USER_PASSWORD}" \
        --allow-root
    
    echo "WordPress configuré avec succès !"
else
    echo "WordPress déjà configuré."
fi

# Ajuster les permissions
echo "Configuration des permissions..."
chown -R www-data:www-data /var/www/html
find /var/www/html -type d -exec chmod 755 {} \;
find /var/www/html -type f -exec chmod 644 {} \;

echo "=== Setup WordPress terminé ==="
echo "Démarrage de PHP-FPM..."

# Démarrer PHP-FPM en foreground
exec php-fpm82 -F
