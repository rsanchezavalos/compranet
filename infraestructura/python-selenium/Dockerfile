FROM ubuntu:16.04
MAINTAINER Roberto Sanchez <r.sanchezavalos@gmail.com>

ENV REFRESHED_AT 2017-04-09


RUN apt-get update; \
  apt-get --yes  install build-essential checkinstall; \
  apt-get --yes install libxss1 libappindicator1 libindicator7; \
  apt-get --yes install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-devsudo ; \
  apt-get --yes install wget unzip curl xvfb xz-utils zlib1g-dev libssl-dev
 
#==================
# Python 2.7.12
#==================

RUN version=2.7.12 && \
  cd ~/Downloads/ && \
  wget https://www.python.org/ftp/python/$version/Python-$version.tgz && \
  Extract and go to the directory: && \
  tar -xvf Python-$version.tgz && \
  cd Python-$version && \
  ./configure && \
  make && \
  sudo make altinstall && \
  alias python=python2.7 && \

ADD  apt-get install -qy python python-dev python-distribute python-pip ipython; \
  apt-get install -qy firefox unzip; \
  pip install selenium xvfbwrapper beautifulsoup4 requests 


#===============
# Google Chrome
#===============
ADD  apt-get update  && \
  apt-get --yes install postgresql-client  && \
  apt-get install libnss3 libgconf-2-4 

#===============
# Google Chrome
#===============

RUN  apt-get install libxss1 libappindicator1 libindicator7 && \
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
  dpkg -i google-chrome*.deb && \
  apt-get install -f && \
  apt-get install xvfb 



#==================
# Chrome webdriver
#==================
ADD  apt-get install unzip && \
  wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip && \
  unzip chromedriver_linux64.zip && \
  chmod +x chromedriver && \
  mv -f chromedriver /usr/local/share/chromedriver && \
  ln -s /usr/local/share/chromedriver /usr/local/bin/chromedriver && \
  ln -s /usr/local/share/chromedriver /usr/bin/chromedriver



ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt


CMD [ "/bin/bash" ]

