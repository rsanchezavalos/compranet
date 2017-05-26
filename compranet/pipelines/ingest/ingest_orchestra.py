#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import random
import os
import ast
import luigi
import glob
import psycopg2
import boto3
import sqlalchemy
import tempfile
import numpy as np
import datetime
import subprocess
import pandas as pn
from luigi import six
from os.path import join, dirname
from luigi import configuration
from luigi.s3 import S3Target, S3Client
from dotenv import load_dotenv,find_dotenv
from compranet.pipelines.utils.declaranet_tools import fill_with_near
from compranet.pipelines.utils.pg_compranet import parse_cfg_list, download_dir
import luigi.task

# Variables de ambiente
load_dotenv(find_dotenv())

# Load Postgres Schemas
temp = open('compranet/pipelines/common/pg_raw_schemas.txt').read()
schemas = ast.literal_eval(temp)
open('compranet/pipelines/common/pg_raw_schemas.txt').close()


# AWS
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

#######################
# Classic Ingest Tasks
#########
# Definición de un Pipeline estandar  -> pipeline_task. 
#######################

class UpdateDB(luigi.postgres.CopyToTable):

    """ 
        Pipeline Clásico -
        Esta Task toma la versión Output de cada pipeline_task y guarda en 
        Postgres una tabla con su nombre para consumo del API.

        ToDo(Dynamic columns -> replace the class variable with a runtime-calculated function using a @property declaration)
        https://groups.google.com/forum/#!msg/luigi-user/FA7MdzXS9IE/RCVculxoviIJ
    """

    pipeline_task = luigi.Parameter()
    year_month = luigi.Parameter()
    
    # RDS Parameters
    database = os.environ.get("PGDATABASE_COMPRANET")
    user = os.environ.get("POSTGRES_USER_COMPRANET")
    password = os.environ.get("POSTGRES_PASSWORD_COMPRANET")
    host = os.environ.get("PGHOST_COMPRANET")

    @property
    def update_id(self):
        num = str(random.randint(0,100000))
        return num + self.pipeline_task 

    @property
    def columns(self):
        return schemas[self.pipeline_task]["SCHEMA"]

    @property
    def table(self):
        return "raw." + self.pipeline_task

    def requires(self):
        
        return UpdateOutput(pipeline_task=self.pipeline_task, year_month=self.year_month)

    def rows(self):

        data = pn.read_csv(self.input().path,sep="|",error_bad_lines = False,encoding="utf-8",dtype=str)       
        #data = data.replace(r'\s+',np.nan,regex=True).replace('',np.nan)
        data = data.replace('nan', np.nan, regex=True)
        data = data.where((pn.notnull(data)), None)

        return [tuple(x) for x in data.to_records(index=False)]

    def run(self):

        if not (self.table and self.columns):
            raise Exception("table and columns need to be specified")

        connection = self.output().connect()
        tmp_dir = luigi.configuration.get_config().get('postgres', 'local-tmp-dir', None)
        tmp_file = tempfile.TemporaryFile(dir=tmp_dir)
        n = 0

        for row in self.rows():
            n += 1   
            rowstr = self.column_separator.join(self.map_column(val) for val in row)
            rowstr += "\n"
            tmp_file.write(rowstr.encode('utf-8'))

        tmp_file.seek(0)

        for attempt in range(2):
            try:
                cursor = connection.cursor()
                self.init_copy(connection)
                self.copy(cursor, tmp_file)
                self.post_copy(connection)
            except psycopg2.ProgrammingError as e:
                if e.pgcode == psycopg2.errorcodes.UNDEFINED_TABLE and attempt == 0:
                    # if first attempt fails with "relation not found", try creating table
                    
                    connection.reset()
                    self.create_table(connection)
                else:
                    raise
            else:
                break
        connection.commit()
        self.output().touch(connection)

        # ToDo(Create uniq index and Foreign keys)
        #index= schemas[self.pipeline_task]["INDEX"]
        #cursor.execute('CREATE INDEX {0}_index ON raw.{1} ({0});'.format(index[0], self.pipeline_task))

        connection.commit()
        self.output().touch(connection)
        # Make the changes to the database persistent
        connection.commit()
        connection.close()
        tmp_file.close()

    def output(self):


        return luigi.postgres.PostgresTarget(host=self.host,database=self.database,user=self.user,
                password=self.password,table=self.table,update_id=self.update_id)

class UpdateOutput(luigi.Task):

    """ 
        Pipeline Clásico - 
        Descarga Bash/Python Almacenamiento en S3 

        Task Actualiza la versión Output de cada PipelineTask
        comparando con la última en raw.

        ToDo(Spark Version) 
    """

    client = luigi.s3.S3Client()
    pipeline_task = luigi.Parameter()
    year_month = luigi.Parameter()
    raw_bucket = luigi.Parameter('DEFAULT')
    local_path = luigi.Parameter('DEFAULT')
    
    def requires(self):

        return LocalToS3(pipeline_task=self.pipeline_task, year_month=self.year_month)

    def run(self):

        output_path = self.raw_bucket + self.pipeline_task + \
            "/output/" + self.pipeline_task + ".csv"


        input_path = self.raw_bucket + self.pipeline_task + "/raw/" + self.year_month + \
        "--" + self.pipeline_task + ".csv"

        local_ingest_file = self.local_path + "/" +self.pipeline_task + "/" +self.pipeline_task  + ".csv"            

        if not self.client.exists(path=output_path):
            self.client.copy(source_path=self.raw_bucket + self.pipeline_task + "/raw/" + self.year_month + 
                "--" + self.pipeline_task + ".csv", destination_path=output_path)
        else:
            obj = s3.get_object(Bucket='dpa-compranet', Key='etl/'+ self.pipeline_task + \
                "/output/" + self.pipeline_task + ".csv")
            
            output_db = pn.read_csv(obj['Body'],sep="|",error_bad_lines = False, dtype=str, encoding="utf-8")
            
            obj = s3.get_object(Bucket='dpa-compranet', Key='etl/'+ self.pipeline_task + \
                 "/raw/" + self.year_month + "--" + self.pipeline_task + ".csv")

            input_db=pn.read_csv(obj['Body'],sep="|",error_bad_lines = False, dtype=str, encoding="utf-8")
            output_db = output_db.append(input_db, ignore_index=True)
            output_db.drop_duplicates(keep='first', inplace=True)
            


            output_db.to_csv(local_ingest_file,sep="|",index=False)


            self.client.remove(self.raw_bucket + self.pipeline_task +
                               "/output/" + self.pipeline_task + ".csv")
            self.client.put(local_path=local_ingest_file,
                               destination_s3_path=self.raw_bucket + self.pipeline_task + "/raw/" + 
                               self.year_month + "--" +
                               self.pipeline_task + ".csv")            

        return True

    def output(self):

        output_path = self.raw_bucket + self.pipeline_task + \
            "/output/" + self.pipeline_task + ".csv"

        return S3Target(path=output_path)

class LocalToS3(luigi.Task):

    """ 
        Pipeline Clásico - 
        Almacena datos descargados de cada
        pipeline task de local al S3 asignado al proyecto.
    """

    year_month = luigi.Parameter()
    # name of task, both scripts and csv will be stored this way
    pipeline_task = luigi.Parameter()

    client = luigi.s3.S3Client()
    local_path = luigi.Parameter('DEFAULT')  # path where csv is located
    raw_bucket = luigi.Parameter('DEFAULT')  # s3 bucket address

    def requires(self):

        local_ingest_file = self.local_path  +self.pipeline_task + ".csv"
        return LocalIngest(self.pipeline_task, self.year_month, local_ingest_file)

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

class LocalIngest(luigi.Task):

    """ 
        Pipeline Clásico - 
        Esta Task permite separar los procesos del Pipeline Clasico
        y llamar scripts específicos por pipeline Task
    """

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
####### 
# Funciones usadas por el LocalIngest para los pipeline 
# tasks del Pipeline Clásico
#######################

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

class claves_salariales(luigi.Task):
    """
    Clase que descarga las claves salariales de los puestos de los funcionarios públicos
    """
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

class declaranet(luigi.Task):

    year_month = luigi.Parameter()
    pipeline_task = luigi.Parameter()
    local_ingest_file = luigi.Parameter()

    def requires(self):

        yield UpdateDB(self.year_month,pipeline_task="funcionarios")
        yield DeclaranetPDFtoText(self.year_month,self.pipeline_task)

    def run(self):

        data_path = '../../data/declaranet/cv_to_text.txt'
        data = pn.read_csv(data_path, sep = '|', error_bad_lines = False,dtype=str,encoding="utf-8")
        data = fill_with_near(data)

        return data.to_csv(self.output().path,index=False, sep="|")

    def output(self):

        return luigi.LocalTarget(self.local_ingest_file)

class DeclaranetPDFtoText(luigi.Task):

    year_month = luigi.Parameter()
    pipeline_task = luigi.Parameter()
    type_script = luigi.Parameter('sh')
    local_path = luigi.Parameter('DEFAULT')

    bash_scripts = luigi.Parameter()

    #def require(self):
    #    return IngestPipeline(self.year_month)

    def run(self):

        cv_path = self.local_path + "declaranet/cv/"
        cv_output_path = self.local_path + "declaranet/cv_output/"
        lista = glob.glob("../../data/declaranet/cv/*.pdf")

        print("Pasando a texto " + str(len(lista)) + " cv's de burócratas" )
        i = 0

        for funcionario in lista:
            i += 1

            cmd = '''
                {0}/{1}.{2} {3}
                '''.format(self.bash_scripts, self.pipeline_task, 
                    self.type_script, funcionario)
            
        return subprocess.call(cmd, shell=True)

    def output(self):

        return luigi.LocalTarget("../../data/declaranet/cv_to_text.txt")

class DeclaranetS3Download(luigi.Task):

    raw_bucket = luigi.Parameter('DEFAULT')
    local_path = luigi.Parameter('DEFAULT')
    client = luigi.s3.S3Client()
    year = luigi.Parameter()
    local = "etl/declaranet/raw/2017/" 

    #def requires(self):
    #    return()


    def run(self):

        cp_cmd = "s3://dpa-compranet/"+self.local

        cmd="""
                docker run --rm --env AWS_ACCESS_KEY_ID={} --env \
                AWS_SECRET_ACCESS_KEY={} compranet/download-declaranet '{}' 
            """.format(aws_access_key_id, aws_secret_access_key, cp_cmd,
                "../../data/declaranet/cv/")

        return subprocess.call(cmd, shell=True)

    def output(self):
        local_path = self.local_path + "declaranet/temp.csv"
        return luigi.LocalTarget(local_path)

class DeclaranetCrawl(luigi.Task):

    """
    Task que hace query a la base de funcionarios para definir la lista de 
    funcionarios a crawlear en Declaranet -> Descarga directamente a S3.

    Dependencias - Pipeline Ingesta: Funcionarios
    """

    client = luigi.s3.S3Client()  

    # ToDo(Definir el update_id del pipelinetask a revisa)
    #def requires(self):
    #    return luigi.postgres.PostgresTarget(host=self.host,database=self.database,user=self.user,
    #            password=self.password,table="funcionarios",update_id=self.update_id)

    def run(self):

        conn = psycopg2.connect(
            dbname = os.environ.get("PGDATABASE_COMPRANET"),
            user = os.environ.get("POSTGRES_USER_COMPRANET"),
            host = os.environ.get("PGHOST_COMPRANET"),
            password = os.environ.get("POSTGRES_PASSWORD_COMPRANET"))

        cur = conn.cursor()

        # Por motivos de presupuesto/tiempo se restringue a secretarías
        cur.execute("""SELECT  
            nombre || primer_apellido || segundo_apellido FROM 
            raw.funcionarios  WHERE institucion LIKE '%SECRETAR%' order by nombre""")

        #logger.info("Descargando Funcionarios")
        rs = []

        funcionarios = cur.fetchall()

        for funcionario in funcionarios:

            yield Declaranet_funcionario(funcionario=list(funcionario)[0])

class DeclaranetFuncionario(luigi.Task): 

    """
    Task que levanta multiples servicios de docker para descargar el currículum de los funcionarios
    de la plataforma Declaranet.
    """

    client = luigi.s3.S3Client()
    today = datetime.date.today()
    year = str(today.year) 

    funcionario=luigi.Parameter()
    bash_scripts = luigi.Parameter('DEFAULT')
    local_path = luigi.Parameter('DEFAULT')
    raw_bucket = luigi.Parameter('DEFAULT')

    def run(self):
   
        print(self.funcionario)
        print(aws_access_key_id)
        # Get funcionarios list

        cmd="""
            docker run --rm --env AWS_ACCESS_KEY_ID={} --env 
            AWS_SECRET_ACCESS_KEY={} compranet/download-declaranet '{}' 
            """.format(aws_access_key_id, aws_secret_access_key, self.funcionario)

        with self.output().open('w') as f:
            f.write('Funcionario: {0}'.format(self.funcionario))

        return subprocess.call(cmd, shell=True)

    def output(self):

        # Output guarda archivo de que ya lo procesó por cada burócrata.

        file = "%s.temp" % self.funcionario
        file.strip().replace(" ","_")

        output_path = self.raw_bucket + "declaranet" + \
            "/raw/" + self.year + "/run/" + file
        
        return S3Target(path=output_path)
