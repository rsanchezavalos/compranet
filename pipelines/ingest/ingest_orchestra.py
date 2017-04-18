import subprocess
import os
from os.path import join, dirname
import luigi
from luigi.s3 import S3Target, S3Client
from luigi.contrib.postgres import PostgresTarget
from luigi import configuration
from utils.pg_compranet import parse_cfg_list
 
 
from dotenv import load_dotenv
## Variables de ambiente
path = os.path.abspath('__file__' + "/../../config/")
dotenv_path = join(path, '.env')
load_dotenv(dotenv_path)
 
## AWS
aws_access_key_id =  os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
## RDS
host = os.environ.get('PGHOST')
database = os.environ.get('PGDATABASE') 
user = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
 
 
class update_dbs(luigi.Task):
    pipeline_task = luigi.Parameter()
    year_month = luigi.Parameter()
    table = pipeline_task
 
    #columns = [("date_from", "DATE"),
    #           ("date_to", "DATE"),
    #           ("artist", "TEXT"),
    #           ("streams", "INT")]
 
    def require(self):
        return bash_ingestion_s3(pipeline_task=pipeline, year_month=self.year_month)
 
    def run():
 
        return
 
    def output(self):
        #ver si ya está en postgres
        return PostgresTarget()
 
 
 
class bash_ingestion_s3(luigi.Task):
    pipeline_task = luigi.Parameter()
    year_month = luigi.Parameter()
 
    client = luigi.s3.S3Client()
 
    bash_scripts =  luigi.Parameter()
 
    local_path =  luigi.Parameter() 
    raw_bucket = luigi.Parameter()
 
    def run(self):
        #Guarda en temp
        bash_command =  self.bash_scripts + self.pipeline_task + '.sh '
        subprocess.call([bash_command], shell=True)
 
        return self.client.put(local_path=self.local_path + self.pipeline_task + ".csv",
            destination_s3_path=self.raw_bucket + self.pipeline_task + "/raw/" + self.year_month +"--"+ self.pipeline_task + ".csv")
 
    def output(self):
        return S3Target(path=self.raw_bucket + self.pipeline_task + "/raw/" +  self.year_month +"--"+ self.pipeline_task + ".csv")
 
 
class update_history_s3(luigi.Task):
 
    def request(self):
        return bash_ingestion_s3()
 
    def run(self):
        return
 
    def outpunt():
        S3Target(path=self.raw_bucket + self.pipeline_task + "/output/" + self.pipeline_task + ".csv")
 
 
 
 
 
 
 
 
 
 
#class docker_ingestion_s3(luigi.Task):
#    def run(self):
#        pass
#    def output(self):
#           pass