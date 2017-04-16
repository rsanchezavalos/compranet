FROM dpa/python:0.1

MAINTAINER Adolfo De Unánue <nanounanue@gmail.com>

ENV LUIGI_HOME /etc/luigi

RUN apt-get update -yq

RUN apt-get install -yqq ssh git build-essential

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir $LUIGI_HOME

CMD [ "/bin/sh", "-c", "while true; do echo hello world; sleep 1; done"]
