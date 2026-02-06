FROM alpine:3.22

# Installation de Nginx et OpenSSL
RUN	apk update &&		\
	apk add --no-cache	\
	nginx			\
	openssl			\
	gettext &&		\
	rm -rf /var/cache/apk/*

# Création des répertoires nécessaires
RUN mkdir -p /etc/nginx/ssl \
    /var/www/html \
    /run/nginx

# Copie de la configuration Nginx
COPY conf/nginx.conf.template /etc/nginx/nginx.conf.template

# Copie du script qui générera le certificat SSL
COPY tools/setup.sh /usr/local/bin/setup.sh
RUN chmod +x /usr/local/bin/setup.sh

EXPOSE 443

# Le script va générer le certificat SSL et démarrer Nginx
ENTRYPOINT ["/usr/local/bin/setup.sh"]
