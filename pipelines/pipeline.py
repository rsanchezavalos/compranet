# coding: utf-8
# Run as: PYTHONPATH='.' luigi --module pipeline Ingestpipelines --local-scheduler
#pip install tornado # luigi uses the tornado web server
#export PATH=$PATH:/home/ubuntu/workspace/luigi/bin
#export PYTHONPATH=/home/ubuntu/workspace/luigi:.
#luigid

import os
from os.path import join, dirname
import logging
import luigi
import luigi.s3
from luigi import configuration
from dotenv import load_dotenv

#import sqlalchemy
#import dummy.config_ini
#import os
#import subprocess
#import pandas as pd
#import csv
#import datetime

logger = logging.getLogger("dpa-compranet.dummy")
from utils.pg_compranet import parse_cfg_string
from ingest.ingest_orchestra import bash_ingestion

path = os.path.abspath('__file__' + "/../../config/")
dotenv_path = join(path, '.env')
load_dotenv(dotenv_path)

class Ingestpipelines(luigi.WrapperTask):
    """
    Ingest Pipeline 
    """

    conf = configuration.get_config()
    #ingest_pipelines = luigi.Parameter()
    ingest_pipelines = parse_cfg_string(conf.get("Ingestpipelines", "ingest_pipelines"))

    def requires(self):
        tasks = []
        for pipeline in self.ingest_pipelines:
            tasks.append(Ingestpipeline(pipeline))
        return tasks


class Ingestpipeline(luigi.WrapperTask):
    """
    This wrapper task executes a single ingest pipeline
    It expects a string specifying which section of the luigi.cfg file to
    extract configuration options from.
    """
    pipeline_task = luigi.Parameter()

    def requires(self):
        return bash_ingestion(self.pipeline_task)


if __name__ == "__main__":
    luigi.run()
