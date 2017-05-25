import os
from os.path import join, dirname
import logging
from dotenv import load_dotenv, find_dotenv
import luigi 
import magic_loop_dpa
import sys
egg_path = '/usr/local/lib/python2.7/site-packages/datasets-0.0.9-py2.7.egg'
sys.path.append(egg_path)
import datasets
logger = logging.getLogger("magic_loop.log")



 
class RunModel(luigi.WrapperTask):
	def requireres(self):
		pass
	def run(self):
		pass

class magic_loop(self):
	iris = datasets.load_iris()

	def run:


		clfs, grid = define_hyper_params()
		models_to_run_GS=['LR', 'AB']
		models_to_run_RS=['KNN','RF','GB','DT']
		encoders = dict()
		X = self.iris.data
		y = self.iris.target
		

		magic_loop(models_to_run_GS, clfs,grid, X,y, cv = 5, ParamTun = 'GridSearchCV')
		
		return


	def output(self):
		pass


