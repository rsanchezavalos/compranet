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
from luigi.contrib.postgres import PostgresTarget, PostgresQuery
from compranet.pipelines.utils.pg_compranet import parse_cfg_list, download_dir
from compranet.pipelines.utils.declaranet_tools import fill_with_near

# Variables de ambiente
load_dotenv(find_dotenv())

# Load Postgres Schemas
#temp = open('./common/pg_clean_schemas.txt').read()
#schemas = ast.literal_eval(temp)

# AWS
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

class ETL(luigi.Task):

    year_month = luigi.Parameter()

    def requires(self):
    	return MergeDBs(self.year_month)

class MergeDBs(luigi.postgres.PostgresQuery):
	year_month = luigi.Parameter()

	sql_scripts = luigi.Parameter('EtlPipeline')
	database = os.environ.get("PGDATABASE_COMPRANET")
	user = os.environ.get("POSTGRES_USER_COMPRANET")
	password = os.environ.get("POSTGRES_PASSWORD_COMPRANET")
	host = os.environ.get("PGHOST_COMPRANET")

	def requires(self):
		return CleanDB(self.year_month)

	@property
	def update_id(self):
		num = str(random.randint(0,100000))
		return num 
	@property
	def table(self):
		return "clean.funcionarios" 
	@property
	def query(self):
		sqlfile = open('./etl/sql_scripts/merge.sql', 'r')
		query = sqlfile.read()
		return query 

	def output(self):
		
		return luigi.postgres.PostgresTarget(host=self.host,database=self.database,user=self.user,
			password=self.password,table=self.table,update_id=self.update_id)

class CleanDB(luigi.postgres.PostgresQuery):
	year_month = luigi.Parameter()

	sql_scripts = luigi.Parameter('EtlPipeline')
	database = os.environ.get("PGDATABASE_COMPRANET")
	user = os.environ.get("POSTGRES_USER_COMPRANET")
	password = os.environ.get("POSTGRES_PASSWORD_COMPRANET")
	host = os.environ.get("PGHOST_COMPRANET")

	@property
	def update_id(self):
		num = str(random.randint(0,100000))
		return num 

	@property
	def table(self):
		return "clean.diccionario_dependencias" 

	@property
	def query(self):
		sqlfile = open('./etl/sql_scripts/clean.sql', 'r')
		query = sqlfile.read()
		return query 

	def output(self):
		
		return luigi.postgres.PostgresTarget(host=self.host,database=self.database,user=self.user,
			password=self.password,table=self.table,update_id=self.update_id)

class PredictiveModel(luigi.Task):

	year_month = luigi.Parameter()


	def run(self):

		return Magicloop(self.year_month)

class MagicLoop(luigi.Task):

	year_month = luigi.Parameter()

	def requires(self):

		return CleanDB(self.pipeline_task, self.year_month)

	def run(self):

		yield print("Running Magicloop")


class SetNeo4J(luigi.Task):

	year_month = luigi.Parameter()

	def requires(self):

		return CleanDB(self.pipeline_task, self.year_month)

	def run(self):


		conn = psycopg2.connect(

		    dbname = os.environ.get("PGDATABASE_COMPRANET"),
		    user = os.environ.get("POSTGRES_USER_COMPRANET"),
		    host = os.environ.get("PGHOST_COMPRANET"),
		    password = os.environ.get("POSTGRES_PASSWORD_COMPRANET"))

		cur = conn.cursor()
		query = """SELECT * FROM raw.compranet LIMIT 10000"""
		outputquery = 'copy ({0}) to stdout with csv header'.format(query)

		with open('../../data/neo4j/compranet.csv', 'w') as f:
		    cur.copy_expert(outputquery, f)

		conn.close()

		return CentralityClassifier(pipeline_task="compranet",year_month=self.year_month)




class MissingClassifier(luigi.Task):

	year_month = luigi.Parameter()

	def requires(self):

		return CleanDB(self.pipeline_task, self.year_month)


	def run(self):

		yield print("Running MissingClassifier")


class CentralityClassifier(luigi.Task):

	year_month = luigi.Parameter()


	def run(self):

		yield print("Running CentralityClassifier")

