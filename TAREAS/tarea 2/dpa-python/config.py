import os
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = "postgresql://docker:docker@dpa_postgres/docker"
