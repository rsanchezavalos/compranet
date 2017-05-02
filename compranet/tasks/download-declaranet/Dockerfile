FROM python-selenium:0.1

ENV PROJECT_NAME declaranet

ADD . /${PROJECT_NAME}/

WORKDIR /${PROJECT_NAME}

RUN pip install click unidecode

RUN curl -LOk https://github.com/rsanchezavalos/burocratas-cv/archive/master.zip

RUN unzip master.zip

WORKDIR /${PROJECT_NAME}/burocratas-cv-master

ADD ./declaranet.py declaranet.py

ENTRYPOINT [ "python", "declaranet.py" ]