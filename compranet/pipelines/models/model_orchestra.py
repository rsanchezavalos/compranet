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
from compranet.pipelines.pipelines.etl.elt_orchestra import CreateSemanticDB

# Variables de ambiente
load_dotenv(find_dotenv())

# Load Postgres Schemas
#temp = open('./common/pg_clean_schemas.txt').read()
#schemas = ast.literal_eval(temp)

# AWS
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

class Model(luigi.Task):

	"""
	Clase intermedia que activa los scripts de modelado
	"""

    year_month = luigi.Parameter()

    def requires(self):

    	return CreateSemanticDB(self.year_month)

    def run(self):

    	yield MissingClassifier(self.year_month)
    	yield CentralityClassifier(self.year_month)



class CentralityClassifier(luigi.Task):

	"""
	Clase que corre las medidas de centralidad implementadas por
	neo4j
	"""

	year_month = luigi.Parameter()
    script = luigi.Parameter('DEFAULT')
    type_script = luigi.Parameter()

    def run(self):

        # Todo() this can be easily dockerized
        cmd = '''
            cycli {}/{}.{}
            '''.format(self.script, self.pipeline_task, self.type_script)


class MissingClassifier(luigi.Task):

	"""
	Clase que corre el índice 
	neo4j
	"""

	year_month = luigi.Parameter()
    script = luigi.Parameter('DEFAULT')

    def run(self):
        
        cmd = '''
            python {}/missing-classifier.py
            '''.format(self.script)

        return subprocess.call(cmd, shell=True)

