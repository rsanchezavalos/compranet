FROM python:3.5-slim

# Contenedor que al ajecutarse obtiene un renglón al azar del dataset y lo imprime en pantalla (puedes construirlo en bash (httpie) o en python

## Actualizamos
RUN \
    apt-get -qq update; apt-get upgrade -y -qq; \
    apt-get install -y --no-install-recommends -qq wget curl git locales bzip2 unzip xz-utils build-essential; \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

## Arreglamos el LOCALE
RUN echo "es_MX.UTF-8 UTF-8" >> /etc/locale.gen \
    && locale-gen es_MX.utf8 \
    && /usr/sbin/update-locale LANG=es_MX.UTF-8 \
    && dpkg-reconfigure locales


RUN apt-get update \
    && apt-get install -y libblas-dev liblapack-dev gfortran \
                       libpq-dev \
                       make libssl-dev zlib1g-dev \
                       libbz2-dev libreadline-dev libsqlite3-dev llvm \
                       libncurses5-dev libncursesw5-dev xz-utils libpng12-dev \
                       libfreetype6-dev libfreetype6 libxft-dev freetype* \
                       libmysqlclient-dev

## Requerimientos
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt


EXPOSE 8090

## Copiar código bash o python
ADD hello_world.py /tmp/hello_world.py

# Correr en bash
CMD [ "python" , "/tmp/hello_world.py"]



