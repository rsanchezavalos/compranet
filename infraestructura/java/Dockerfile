FROM dpa/base:0.1

MAINTAINER Adolfo De Unánue <nanounanue@gmail.com>

ENV REFRESHED_AT 2017-03-10

## NOTE: Casi todo lo que sigue está copiado del Dockerfile de openjdk:8

# Script para configurar JAVA_HOME
RUN { \
		echo '#!/bin/sh'; \
		echo 'set -e'; \
		echo; \
		echo 'dirname "$(dirname "$(readlink -f "$(which javac || which java)")")"'; \
	} > /usr/local/bin/docker-java-home \
	&& chmod +x /usr/local/bin/docker-java-home


RUN echo 'deb http://deb.debian.org/debian jessie-backports main' > /etc/apt/sources.list.d/jessie-backports.list

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

ENV JAVA_VERSION 8u111

ENV JAVA_DEBIAN_VERSION 8u121-b13-1~bpo8+1

# Debido a https://bugs.debian.org/775775
# y https://github.com/docker-library/java/issues/19#issuecomment-70546872
ENV CA_CERTIFICATES_JAVA_VERSION 20161107~bpo8+1

RUN set -x \
    && apt-get update \
    && apt-get  install -y \
       openjdk-8-jdk="$JAVA_DEBIAN_VERSION" \
       ca-certificates-java="$CA_CERTIFICATES_JAVA_VERSION" \
    && rm -rf /var/lib/apt/lists/* \
    && [ "$JAVA_HOME" = "$(docker-java-home)" ]

RUN /var/lib/dpkg/info/ca-certificates-java.postinst configure


CMD ["/bin/bash"]
