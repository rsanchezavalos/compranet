import subprocess
import os
import luigi
from luigi import configuration
from utils.pg_compranet import parse_cfg_string


class bash_ingestion(luigi.Task):
    pipeline_task = luigi.Parameter()

    def run(self):
    	conf = configuration.get_config()
    	bash_path = parse_cfg_string(conf.get("etl", "bash_path"))
    	bash_command =  str(bash_path[0]) + "/"+str(self.pipeline_task) + '.sh '
    	print(bash_command)
    	subprocess.call([bash_command], shell=True)
    	return 

    def output(self):
        return luigi.LocalTarget("../data/temp/" + str(self.pipeline_task) + ".csv")
