FROM alpine:3.22

# Installation de PHP-FPM et extensions WordPress
RUN apk update && \
	apk add --no-cache \
	php82 \
	php82-fpm \
	php82-mysqli \
	php82-json \
	php82-curl \
	php82-dom \
	php82-exif \
	php82-fileinfo \
	php82-mbstring \
	php82-openssl \
	php82-xml \
	php82-zip \
	php82-redis \
	php82-phar \
	php82-session \
	php82-iconv \
	php82-gd \
	php82-zlib \
	wget \
 	curl \
	netcat-openbsd && \
	rm -rf /var/cache/apk/*

# Augmenter la mémoire PHP pour WP-CLI
RUN echo "memory_limit = 256M" > /etc/php82/conf.d/99-memory-limit.ini

# Symlink pour wp-cli
RUN ln -s /usr/bin/php82 /usr/bin/php

# Créer un user pour php-fpm
RUN adduser -D -S -G www-data www-data

# Création du répertoire WordPress
RUN mkdir -p /var/www/html

# Configuration PHP-FPM pour écouter sur le réseau
RUN sed -i 's|listen = 127.0.0.1:9000|listen = 9000|g' /etc/php82/php-fpm.d/www.conf && \
	sed -i 's|;clear_env = no|clear_env = no|g' /etc/php82/php-fpm.d/www.conf && \
	sed -i 's|user = nobody|user = www-data|g' /etc/php82/php-fpm.d/www.conf && \
	sed -i 's|group = nobody|group = www-data|g' /etc/php82/php-fpm.d/www.conf

# Installation de WP-CLI
RUN wget https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && \
    chmod +x wp-cli.phar && \
    mv wp-cli.phar /usr/local/bin/wp

# Copie du script de setup
COPY tools/setup.sh /usr/local/bin/setup.sh
RUN chmod +x /usr/local/bin/setup.sh

WORKDIR /var/www/html

EXPOSE 9000

# Le script va télécharger WordPress, le configurer et démarrer PHP-FPM
ENTRYPOINT ["/usr/local/bin/setup.sh"]
