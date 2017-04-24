import subprocess
import os
import pandas as pd
from os.path import join, dirname
import luigi
from luigi.s3 import S3Target, S3Client
#from luigi.contrib.postgres import PostgresTarget
from luigi import configuration
from utils.pg_compranet import parse_cfg_list

from dotenv import load_dotenv
# Variables de ambiente
path = os.path.abspath('__file__' + "/../../config/")
dotenv_path = join(path, '.env')
load_dotenv(dotenv_path)

# AWS
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')


class classic_pipeline(luigi.Task):
    client = luigi.s3.S3Client()
    pipeline_task = luigi.Parameter()
    year_month = luigi.Parameter()
    raw_bucket = luigi.Parameter('DEFAULT')
    local_path = luigi.Parameter('DEFAULT')

    def requires(self):
        return local_to_s3(pipeline_task=self.pipeline_task, year_month=self.year_month)

    def run(self):
        # todo() Función aún sin sentido, copia y pega a output
        output_path = self.raw_bucket + self.pipeline_task + \
            "/output/" + self.pipeline_task + ".csv"

        if not self.client.exists(path=output_path):
            self.client.copy(source_path=self.raw_bucket +
                             self.pipeline_task + "/raw/" + self.year_month +
                             "--" + self.pipeline_task + ".csv",
                             destination_path=output_path)

        else:
            self.client.get(path=output_path,
                            destination_local_path=self.local_path + self.pipeline_task + "output.csv")
            self.client.remove(self.raw_bucket + self.pipeline_task +
                               "/output/" + self.pipeline_task + ".csv")
            self.client.put(self.local_path +
                            self.pipeline_task + "output.csv", output_path)
        return True

    def output(self):
        output_path = self.raw_bucket + self.pipeline_task + \
            "/output/" + self.pipeline_task + ".csv"
        return S3Target(path=output_path)


class local_to_s3(luigi.Task):
    year_month = luigi.Parameter()
    # name of task, both scripts and csv will be stored this way
    pipeline_task = luigi.Parameter()

    client = luigi.s3.S3Client()
    local_path = luigi.Parameter('DEFAULT')  # path where csv is located
    raw_bucket = luigi.Parameter('DEFAULT')  # s3 bucket address

    def requires(self):
        local_ingest_file = self.local_path + \
            "/" +self.pipeline_task + ".csv"
        return local_ingest(self.pipeline_task, self.year_month, local_ingest_file)

    def run(self):
        local_ingest_file = self.local_path + \
            "/" +self.pipeline_task + ".csv"
        return self.client.put(local_path=local_ingest_file,
                               destination_s3_path=self.raw_bucket + self.pipeline_task + "/raw/" + 
                               self.year_month + "--" +
                               self.pipeline_task + ".csv")

    def output(self):
        return S3Target(path=self.raw_bucket + self.pipeline_task + "/raw/" + self.year_month + "--" +
                        self.pipeline_task + ".csv")


class local_ingest(luigi.Task):
    pipeline_task = luigi.Parameter()
    year_month = luigi.Parameter()
    local_ingest_file = luigi.Parameter()

    def requires(self):

        classic_tasks = eval(self.pipeline_task)

        return classic_tasks(year_month=self.year_month, pipeline_task=self.pipeline_task,
                             local_ingest_file=self.local_ingest_file)

    def output(self):

        return luigi.LocalTarget(self.local_ingest_file)


#######################
# Classic Ingest Tasks
#######################

class claves_salariales(luigi.Task):
    # Las clases específicas definen el tipo de llamada por hacer
    client = luigi.s3.S3Client()
    year_month = luigi.Parameter()
    pipeline_task = luigi.Parameter()
    local_ingest_file = luigi.Parameter()
    type_script = luigi.Parameter('sh')

    bash_scripts = luigi.Parameter('DEFAULT')
    local_path = luigi.Parameter('DEFAULT')
    raw_bucket = luigi.Parameter('DEFAULT')

    def run(self):
        # Todo() this can be easily dockerized

        cmd = '''
            {}/{}.{}
            '''.format(self.bash_scripts, self.pipeline_task, self.type_script)

        return subprocess.call(cmd, shell=True)

    def output(self):

        return luigi.LocalTarget(self.local_ingest_file)

class compranet(luigi.Task):
    # Las clases específicas definen el tipo de llamada por hacer
    client = luigi.s3.S3Client()
    year_month = luigi.Parameter()
    pipeline_task = luigi.Parameter()
    local_ingest_file = luigi.Parameter()
    type_script = luigi.Parameter('sh')

    bash_scripts = luigi.Parameter('DEFAULT')
    local_path = luigi.Parameter('DEFAULT')
    raw_bucket = luigi.Parameter('DEFAULT')

    def run(self):
        # Todo() this can be easily dockerized

        cmd = '''
            {}/{}.{}
            '''.format(self.bash_scripts, self.pipeline_task, self.type_script)

        return subprocess.call(cmd, shell=True)

    def output(self):

        return luigi.LocalTarget(self.local_ingest_file)


class unidades_compradoras(luigi.Task):
    # Las clases específicas definen el tipo de llamada por hacer
    client = luigi.s3.S3Client()
    year_month = luigi.Parameter()
    pipeline_task = luigi.Parameter()
    local_ingest_file = luigi.Parameter()
    type_script = luigi.Parameter('sh')

    bash_scripts = luigi.Parameter('DEFAULT')
    local_path = luigi.Parameter('DEFAULT')
    raw_bucket = luigi.Parameter('DEFAULT')

    def run(self):
        # Todo() this can be easily dockerized

        cmd = '''
            {}/{}.{}
            '''.format(self.bash_scripts, self.pipeline_task, self.type_script)

        return subprocess.call(cmd, shell=True)

    def output(self):

        return luigi.LocalTarget(self.local_ingest_file)

class funcionarios(luigi.Task):
    # Las clases específicas definen el tipo de llamada por hacer
    client = luigi.s3.S3Client()
    year_month = luigi.Parameter()
    pipeline_task = luigi.Parameter()
    local_ingest_file = luigi.Parameter()
    type_script = luigi.Parameter('sh')

    bash_scripts = luigi.Parameter('DEFAULT')
    local_path = luigi.Parameter('DEFAULT')
    raw_bucket = luigi.Parameter('DEFAULT')

    def run(self):
        # Todo() this can be easily dockerized

        cmd = '''
            {}/{}.{}
            '''.format(self.bash_scripts, self.pipeline_task, self.type_script)

        return subprocess.call(cmd, shell=True)

    def output(self):

        return luigi.LocalTarget(self.local_ingest_file)

#######################
# Classic Ingest Tasks
#######################


class update_dbs(luigi.postgres.CopyToTable):
    pipeline_task = luigi.Parameter()
    year_month = luigi.Parameter()
    table = "unidades_compradoras_test"
    # RDS
    host = os.environ.get('PGHOST_PREDICTIVA')
    database = os.environ.get('PGDATABASE_PREDICTIVA')
    user = os.environ.get('POSTGRES_USER_PREDICTIVA')
    password = os.environ.get('POSTGRES_PASSWORD_PREDICTIVA')

    columns = [("ID_DEP_ENT", "INT"),
               ("SIGLAS", "TEXT"),
               ("DEPENDENCIA_ENTIDAD", "TEXT"),
               ("RAMO", "TEXT"),
               ("CLAVE_CNET30", "TEXT"),
               ("CLAVE_UC", "TEXT"),
               ("NOMBRE_UC", "TEXT"),
               ("RFC", "TEXT"),
               ("ESTADO", "TEXT"),
               ("DELEGACION_MUNICIPIO", "TEXT"),
               ("TELEFONO_UC", "TEXT"),
               ("DIRECCION", "TEXT"),
               ("CP", "TEXT"),
               ("PAGINA_WEB", "TEXT"),
               ("TIPO", "TEXT"),
               ("ZONA_HORARIA", "TEXT"),
               ("RESPONSABLE", "TEXT"),
               ("PUESTO", "TEXT")]

    def requires(self):
        return bash_ingestion_s3(pipeline_task=self.pipeline_task, year_month=self.year_month)

    def run(self):

        # read in file as list
        print("************************")
        print(self.input())
        print("************************")

    # def run(self):
        # print(self.input())
        # print("*********************")
        #df = pd.read_csv(self.input().path)
        # print(df)
        # return update_history_s3(pipeline_task=self.pipeline_task,
        # year_month=self.year_month)
