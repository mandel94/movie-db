FROM postgres as base 


# Create a new image from the base image

COPY additional_init_files/ /docker-entrypoint-initdb.d/
COPY postgresql.conf /etc/postgresql/postgresql.conf

