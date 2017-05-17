FROM ubuntu:16.04
MAINTAINER Roberto Sanchez <r.sanchezavalos@gmail.com>


ENV REFRESHED_AT 2017-04-09
ENV CHROMEDRIVER_URL=http://chromedriver.storage.googleapis.com/2.25/chromedriver_linux64.zip

RUN apt-get update && \ 
  apt-get install -y --no-install-recommends apt-utils

RUN apt-get -y install python-pip

RUN apt-get -y install chromium-chromedriver

RUN apt-get update; \
  apt-get --yes  install build-essential checkinstall && \
  apt-get --yes install libxss1 libappindicator1 libindicator7  && \
  apt-get --yes install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev && \
  apt-get --yes install wget unzip curl xvfb xz-utils zlib1g-dev libssl-dev

RUN apt-get --yes install libxss1 libappindicator1 libindicator7 libpango1.0-0 fonts-liberation

#==================
# Python 2.7.12
#==================
ENV version=2.7.12 

#RUN  mkdir ~/Downloads/ && \
#  cd ~/Downloads/  

RUN wget https://www.python.org/ftp/python/$version/Python-$version.tgz && \
  tar -xvf Python-$version.tgz && \
  cd Python-$version && \
  ./configure && \
  make && \
  make altinstall && \
  alias python=python2.7 


RUN apt-get update && apt-get install -y \
  python \
  python-dev\
  python-distribute \
  ipython \
  unzip 


RUN apt-get --yes install libxss1 libappindicator1 libindicator7 && \
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb &&\
  dpkg -i google-chrome*.deb


RUN apt-get --yes install -f && \
  apt-get --yes install xvfb && \
  apt-get --yes install unzip

RUN wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip &&\
  unzip chromedriver_linux64.zip &&\
  chmod +x chromedriver

RUN  mv -f chromedriver /usr/local/share/chromedriver &&\
  ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver &&\
  ln -s /usr/local/share/chromedriver /usr/bin/chromedriver &&\
  apt-get --yes install python-pip


#RUN apt-get update &&\
#  apt-get -y install xorg default-jre rungetty gtk2-engines-pixbuf 



ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt


CMD [ "/bin/bash" ]




