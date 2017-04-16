FROM python:3.5-slim

MAINTAINER Adolfo De Unánue <nanounanue@gmail.com>

ENV REFRESHED_AT 2017-01-06

## Actualizamos
RUN \
    apt-get -qq update; apt-get upgrade -y -qq; \
    apt-get install -y --no-install-recommends -qq curl locales bzip2 unzip xz-utils build-essential; \
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


ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt


CMD [ "/bin/bash" ]
