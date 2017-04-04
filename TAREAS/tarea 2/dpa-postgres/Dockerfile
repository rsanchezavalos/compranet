FROM postgres:latest

ENV POSTGRES_DB docker

ADD /scripts/ /docker-entrypoint-initdb.d/
RUN chmod 0755 /docker-entrypoint-initdb.d/iris.sql

RUN echo "host all  all    0.0.0.0/0  md5" >> /var/lib/postgresql/pg_hba.conf
RUN echo "listen_addresses='*'" >> /var/lib/postgresql/postgresql.conf
EXPOSE 5432
