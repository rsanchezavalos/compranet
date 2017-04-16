FROM dpa/python:0.1

MAINTAINER Adolfo De Unánue <nanounanue@gmail.com>

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir /etc/luigi
ADD luigi.cfg /etc/luigi/luigi.cfg
ADD logging.cfg /etc/luigi/logging.cfg
VOLUME /etc/luigi

RUN mkdir /var/log/luigid
ADD logrotate.cfg /etc/logrotate.d/luigid
VOLUME /var/log/luigid

RUN mkdir -p /luigid/state
VOLUME /luigid/state

CMD ["/usr/local/bin/luigid"]
EXPOSE 8082

RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*
