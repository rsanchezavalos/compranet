# coding: utf-8
# Run as: PYTHONPATH='.' luigi --module pipeline Ingestpipelines --workers 4 

import os
import datetime
from os.path import join, dirname
import logging
from dotenv import load_dotenv, find_dotenv
import boto3
import luigi
import luigi.s3
from luigi.s3 import S3Target, S3Client
from luigi import configuration
from joblib import Parallel, delayed
import multiprocessing

logger = logging.getLogger("dpa-compranet.compranet")
from ingest.ingest_orchestra import classic_pipeline, update_dbs, Declaranet
from utils.pg_compranet import parse_cfg_list
 
## Variables de ambiente
load_dotenv(find_dotenv())

 
## Obtenemos las llaves de AWS
aws_access_key_id =  os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
 
class RunPipelines(luigi.WrapperTask):
    """
    Task principal para el pipeline 
    """
    # Pipeline corre mensualmente
    #start_year_month= el pipe de adolfo incluye un start month -> ver rita
    today = datetime.date.today()
    year_month = str(today.year) + "-"+ str(today.month)
    year_month_day = year_month + "-" + str(today.day)

    def requires(self):
        yield Ingestpipeline(self.year_month)


class Ingestpipeline(luigi.WrapperTask):
    """
    This wrapper task executes ingest pipeline
    It expects a list specifying which ingest pipelines to run
    """

    year_month = luigi.Parameter()
    conf = configuration.get_config()
    pipelines = parse_cfg_list(conf.get("Ingestpipeline", "pipelines"))
    #python_pipelines = parse_cfg_list(conf.get("Ingestpipeline", "python_pipelines"))
    num_cores = multiprocessing.cpu_count()

    def requires(self):
        yield Parallel(n_jobs=self.num_cores)(delayed(update_dbs)(pipeline_task=pipeline_task, year_month=self.year_month) for 
        pipeline_task in self.pipelines)

 
class RunDeclaranet(luigi.WrapperTask):
    def requires(self):
        return Declaranet()


if __name__ == "__main__":
    luigi.run()