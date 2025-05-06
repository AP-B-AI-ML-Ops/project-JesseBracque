FROM postgres:15

RUN echo "initialising database..."

COPY ./init.sql /docker-entrypoint-initdb.d/
