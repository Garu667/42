#!/bin/sh

# Chargement des secrets
DB_ROOT_PASSWORD=$(cat /run/secrets/db_root_password)
DB_PASSWORD=$(cat /run/secrets/db_password)

# Vérifier si la base de données existe déjà
if [ ! -d "/var/lib/mysql/mysql" ]; then
    echo "Initialisation de la base de données MariaDB..."
    
    # Initialiser la base de données
    mysql_install_db --user=mysql --datadir=/var/lib/mysql > /dev/null
    
    # Démarrer temporairement MySQL pour la configuration
    mysqld --user=mysql --bootstrap << EOF
USE mysql;
FLUSH PRIVILEGES;

-- Sécuriser l'installation
DELETE FROM mysql.user WHERE User='';
DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');
DROP DATABASE IF EXISTS test;
DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';

-- Créer le root password
ALTER USER 'root'@'localhost' IDENTIFIED BY '${DB_ROOT_PASSWORD}';

-- Créer la base de données WordPress
CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Créer l'utilisateur WordPress et lui donner les permissions
CREATE USER IF NOT EXISTS '${MYSQL_USER}'@'%' IDENTIFIED BY '${DB_PASSWORD}';
GRANT ALL PRIVILEGES ON ${MYSQL_DATABASE}.* TO '${MYSQL_USER}'@'%';

FLUSH PRIVILEGES;
EOF

    echo "Base de données initialisée avec succès !"
else
    echo "Base de données déjà initialisée."
fi

# Démarrer MariaDB en foreground
echo "Démarrage de MariaDB..."
exec mysqld --user=mysql --console
