# coding: utf-8

import re
import os
import ast
import luigi
import psycopg2
import boto3
import random
import sqlalchemy
import tempfile
import glob
import datetime
import subprocess
import pandas as pn
from luigi import six
from os.path import join, dirname
from luigi import configuration
from luigi.s3 import S3Target, S3Client
from dotenv import load_dotenv,find_dotenv
from luigi.contrib import postgres

from compranet.pipelines.pipelines.utils.pg_compranet import parse_cfg_string, download_dir




# Variables de ambiente
load_dotenv(find_dotenv())

# Load Postgres Schemas
#temp = open('./common/pg_clean_schemas.txt').read()
#schemas = ast.literal_eval(temp)

# AWS
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

class Model(luigi.Task):

    year_month = luigi.Parameter()

    def requires(self):

    	return CreateSemanticDB(self.year_month)

    def run(self):

    	yield MissingClassifier(self.year_month)
    	yield Centralitymeasures(self.year_month)
