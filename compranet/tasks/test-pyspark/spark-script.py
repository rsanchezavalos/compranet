# -*- coding: utf-8 -*-

import sys

import click

from pyspark.sql import SparkSession

@click.command()
@click.option('--master')
@click.option('--input', type=click.Path())
@click.option('--output', type=click.Path())
def data_science_thingy(master, input, output):
    sparkSession = SparkSession.builder\
                   .master(master)\
                   .appName("hola mundo desde pyspark")\
                   .getOrCreate()

    df = sparkSession.read.json(input)

    df.show()

    df.createOrReplaceTempView("hola_mundo_desde_pyspark")

    df.cache()

    positivos = sparkSession.sql("select * from hola_mundo_desde_pyspark where numeros > 0")

    positivos.show()

    df.write.parquet(output, mode='overwrite')



if __name__ == "__main__":
    data_science_thingy()
    

