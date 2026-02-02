FROM mysql:8.0

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=inacap_db
ENV MYSQL_USER=inacap_user
ENV MYSQL_PASSWORD=inacap_password

# Copiar scripts SQL para inicializar la BD
COPY database/schema/core/*.sql /docker-entrypoint-initdb.d/01_core/
COPY database/schema/bridge/*.sql /docker-entrypoint-initdb.d/02_bridge/
COPY database/seed_data/*.sql /docker-entrypoint-initdb.d/03_seed/

EXPOSE 3306
