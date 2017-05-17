#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities used throughout Compranet pipeline
"""
import os
import string
import datetime
import psycopg2
import numpy as np
import pandas as pd
import boto3
#import json
#import re
#import hashlib
#import logging
#import logging.config
#from pandas.compat import range, lzip, map
 
import luigi
import luigi.postgres
from luigi import configuration
from luigi import six
 
 
#LOGGING_CONF = configuration.get_config().get("core", "logging_conf_file")
#logging.config.fileConfig(LOGGING_CONF)
#logger = logging.getLogger("compranet.pipeline")
 

 
def parse_cfg_list(string):
    """
    Parse string from cfg into a list
    """
    string = string.split(",")
    return [m.strip() for m in string]
 
 
 
class TableCopyToS3(luigi.Task):
    """Dump a table from postgresql to S3."""
    table_name = luigi.Parameter()
    s3_path = luigi.Parameter()
 
    def output(self):
        return luigi.s3.S3Target(self.s3_path)
 
    def run(self):
        postgres_url = os.environ['POSTGRES_URL']
        url_parts = urlparse.urlparse(postgres_url)
 
        conn = psycopg2.connect(
                host=url_parts.hostname,
                port=url_parts.port,
                user=url_parts.username,
                password=url_parts.password,
                dbname=url_parts.path[1:])
 
        with self.output().open('w') as s3_file:
            conn.cursor().copy_to(s3_file, self.table_name)
 
        conn.close()




def download_dir(client, resource, dist, local='/tmp', bucket='your_bucket'):

    paginator = client.get_paginator('list_objects')

    for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):

        if result.get('CommonPrefixes') is not None:

            for subdir in result.get('CommonPrefixes'):

                download_dir(client, resource, subdir.get('Prefix'), local, bucket)

        if result.get('Contents') is not None:

            for file in result.get('Contents'):

                if not os.path.exists(os.path.dirname(local + os.sep + file.get('Key'))):

                     os.makedirs(os.path.dirname(local + os.sep + file.get('Key')))

                resource.meta.client.download_file(bucket, file.get('Key'), local + os.sep + file.get('Key'))

