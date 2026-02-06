FROM alpine:3.22

# Installation de MariaDB
RUN apk update && \
    apk add --no-cache \
    mariadb \
    mariadb-client && \
    rm -rf /var/cache/apk/*

# Création des répertoires nécessaires
RUN mkdir -p /var/lib/mysql /run/mysqld && \
    chown -R mysql:mysql /var/lib/mysql /run/mysqld

# Copie de la configuration MariaDB
COPY conf/my.cnf /etc/my.cnf

# Copie du script d'initialisation
COPY tools/setup.sh /usr/local/bin/setup.sh
RUN chmod +x /usr/local/bin/setup.sh

EXPOSE 3306

# Le script setup.sh va initialiser la DB et démarrer MariaDB
ENTRYPOINT ["/usr/local/bin/setup.sh"]
