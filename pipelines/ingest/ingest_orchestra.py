import subprocess
import os
from luigi import configuration
from utils.pg_compranet import parse_cfg_string

def bash_ingestion(pipeline_task):
	conf = configuration.get_config()
	bash_path = parse_cfg_string(conf.get("etl", "bash_path"))
	print(os.getcwd())

	bash_command =  str(bash_path[0]) + "/"+str(pipeline_task) + '.sh'
	subprocess.call([bash_command], shell=True)
	return print(str(pipeline_task))