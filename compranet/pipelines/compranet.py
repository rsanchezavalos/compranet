# coding: utf-8
# For now Run as: PYTHONPATH='.' luigi --module pipeline RunPipelines --workers 30

import os
import datetime
from os.path import join, dirname
import logging
from dotenv import load_dotenv, find_dotenv
import boto3
import luigi
import ast
import luigi.s3
from luigi.s3 import S3Target, S3Client
from luigi import configuration
from joblib import Parallel, delayed
import multiprocessing
from compranet.pipelines.ingest.ingest_orchestra import UpdateDB
from compranet.pipelines.etl.etl_orchestra import MissingClassifier, SetNeo4J, PredictiveModel, ETL
from compranet.pipelines.utils.pg_compranet import parse_cfg_list
 
## Variables de ambiente
load_dotenv(find_dotenv())
 
## AWS
aws_access_key_id =  os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
 
class RunPipelines(luigi.WrapperTask):

    """ 
        Master Wrapper de Compranet Pipeline.

    """

    today = datetime.date.today()
    year_month = str(today.year) + "-"+ str(today.month)
    year_month_day = year_month + "-" + str(today.day)

    def requires(self):

        yield IngestPipeline(self.year_month)
        yield EtlPipeline(self.year_month)


class IngestPipeline(luigi.WrapperTask):

    """
        Este wrapper ejecuta la ingesta de cada pipeline-task

    Input Args (From luigi.cfg):
        pipelines: lista con los pipeline-tasks especificados a correr.

    """

    year_month = luigi.Parameter()
    conf = configuration.get_config()
    pipelines = parse_cfg_list(conf.get("IngestPipeline", "pipelines"))
    #python_pipelines = parse_cfg_list(conf.get("IngestPipeline", "python_pipelines"))

    def requires(self):

        for pipeline_task in self.pipelines:

            yield UpdateDB(pipeline_task=pipeline_task, year_month=self.year_month)

class EtlPipeline(luigi.WrapperTask):

    """
        Este wrapper ejecuta el ETL de cada pipeline-task
        Input - lista con los pipeline-tasks especificados a correr.
    """

    year_month = luigi.Parameter()

    def requires(self):

        yield IngestPipeline(self.year_month) 

    def run(self):
        yield ETL(year_month=self.year_month)


class ModelPipeline(luigi.WrapperTask):

    """
        Este wrapper ejecuta los modelos
    """

    year_month = luigi.Parameter()
    conf = configuration.get_config()

    def requires(self):

        yield MissingClassifier(year_month=self.year_month)
        yield SetNeo4J(year_month=self.year_month)
        yield PredictiveModel(year_month=self.year_month)




if __name__ == "__main__":

    luigi.run()