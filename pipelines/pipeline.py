# coding: utf-8
# Run as: PYTHONPATH='.' luigi --module pipeline Ingestpipelines --local-scheduler
 
import os
import datetime
from os.path import join, dirname
import logging
from dotenv import load_dotenv
import boto3
import luigi
import luigi.s3
from luigi.s3 import S3Target, S3Client
from luigi import configuration
 
logger = logging.getLogger("dpa-compranet.dummy")
from utils.pg_compranet import parse_cfg_list
from ingest.ingest_orchestra import update_dbs
 
## Variables de ambiente
path = os.path.abspath('__file__' + "/../../config/")
dotenv_path = join(path, '.env')
load_dotenv(dotenv_path)
 
## Obtenemos las llaves de AWS
aws_access_key_id =  os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
 
 
class RunPipelines(luigi.WrapperTask):
    """
    Task principal para el pipeline 
    """
    # Pipeline corre mensualmente
    #start_year_month= el pipe de adolfo incluye un start month -> ver rita
    year_month = str(datetime.date.today().year) + "-"+ str(datetime.date.today().month)
 
    def requires(self):
        yield Ingestpipeline(self.year_month)
 
 
class Ingestpipeline(luigi.WrapperTask):
    """
    This wrapper task executes ingest pipeline
    It expects a list specifying which ingest pipelines to run
    """
    year_month = luigi.Parameter()
 
    conf = configuration.get_config()
    bash_pipelines = parse_cfg_list(conf.get("Ingestpipeline", "bash_pipelines"))
    #docker_pipelines = parse_cfg_list(conf.get("Ingestpipeline", "docker_pipelines"))
 
    def requires(self):
        for pipeline in self.bash_pipelines:
            yield update_dbs(pipeline_task=pipeline, year_month=self.year_month)
 
        #for pipeline in self.docker_pipelines:
        #    yield docker_ingestion_s3(pipeline)
 
 
 
 
 
if __name__ == "__main__":
    luigi.run()