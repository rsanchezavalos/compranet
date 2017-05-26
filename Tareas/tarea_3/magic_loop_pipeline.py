import logging
import luigi 
import sys
import pandas as pd
import numpy as np
import random
import time
import numpy as np
from luigi import configuration
from sklearn import preprocessing, cross_validation, svm, metrics, tree, decomposition, svm
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression, Perceptron, SGDClassifier, OrthogonalMatchingPursuit, RandomizedLogisticRegression
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.grid_search import ParameterGrid
from sklearn.metrics import *
from sklearn.preprocessing import StandardScaler
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV

import logging.config
logger = logging.getLogger("magic_loop.log")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('example.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
logger.addHandler(fh)


def define_hyper_params():
    """
        Esta función devuelve un diccionario con
        los clasificadores que vamos a utilizar y
        una rejilla de hiperparámetros
    """
    clfs = {
        'RF': RandomForestClassifier(n_estimators=50, n_jobs=-1),
        'ET': ExtraTreesClassifier(n_estimators=10, n_jobs=-1, criterion='entropy'),
        'AB': AdaBoostClassifier(DecisionTreeClassifier(max_depth=1), algorithm="SAMME", n_estimators=200),
        'LR': LogisticRegression(penalty='l1', C=1e5),
        'SVM': svm.SVC(kernel='linear', probability=True, random_state=0),
        'GB': GradientBoostingClassifier(learning_rate=0.05, subsample=0.5, max_depth=6, n_estimators=10),
        'NB': GaussianNB(),
        'DT': DecisionTreeClassifier(),
        'SGD': SGDClassifier(loss="hinge", penalty="l2"),
        'KNN': KNeighborsClassifier(n_neighbors=3) 
            }

    grid = { 
    'RF':{'n_estimators': [1,10,100,1000,10000], 'max_depth': [1,5,10,20,50,100], 'max_features': ['sqrt','log2'],'min_samples_split': [2,5,10]},
    'LR': { 'penalty': ['l1','l2'], 'C': [0.00001,0.0001,0.001,0.01,0.1,1,10]},
    'SGD': { 'loss': ['hinge','log','perceptron'], 'penalty': ['l2','l1','elasticnet']},
    'ET': { 'n_estimators': [1,10,100,1000,10000], 'criterion' : ['gini', 'entropy'] ,'max_depth': [1,5,10,20,50,100], 'max_features': ['sqrt','log2'],'min_samples_split': [2,5,10]},
    'AB': { 'algorithm': ['SAMME', 'SAMME.R'], 'n_estimators': [1,10,100,1000,10000]},
    'GB': {'n_estimators': [1,10,100,1000,10000], 'learning_rate' : [0.001,0.01,0.05,0.1,0.5],'subsample' : [0.1,0.5,1.0], 'max_depth': [1,3,5,10,20,50,100]},
    'NB' : {},
    'DT': {'criterion': ['gini', 'entropy'], 'max_depth': [1,5,10,20,50,100], 'max_features': ['sqrt','log2'],'min_samples_split': [2,5,10]},
    'SVM' :{'C' :[0.00001,0.0001,0.001,0.01,0.1,1,10],'kernel':['linear']},
    'KNN' :{'n_neighbors': [1,5,10,25,50],'weights': ['uniform','distance'],'algorithm': ['auto','ball_tree','kd_tree']}
           }

    return clfs, grid


def parse_cfg_list(string):
    """
    Parse string from cfg into a list
    """
    string = string.split(",")

    return [m.strip() for m in string]

class RunModel(luigi.WrapperTask):

	conf = configuration.get_config()
	models_to_run = parse_cfg_list(conf.get("RunModel", "models_to_run"))

	def requires(self):

		iris = sklearn.datasets.load_iris()

		return SetUp(self.iris,self.models_to_run)

class SetUp(luigi.Task):

	models_to_run= luigi.Parameter()
	iris=luigi.Parameter()

	def run(self):
		clfs, grid = define_hyper_params()
		encoders = dict()
		X = self.iris.data
		y = self.iris.target

		for n in range(1, 2):
			X_train, X_test, y_train, y_test = train_test_split(X, y)
			for index, clf in enumerate([clfs[x] for x in self.models_to_run]):
				logger.debug(self.models_to_run[index])
				print(self.models_to_run[index])
				parameter_values = grid[self.models_to_run[index]]

				yield MagicLoop(X_train, X_test, y_train, y_test, parameter_values,cv)


class MagicLoop(luigi.Task):
	
	X_train = luigi.Parameter()
	X_test = luigi.Parameter()
	y_train = luigi.Parameter()
	y_test = luigi.Parameter()
	parameter_values = luigi.Parameter()
	cv = luigi.Parameter()    
	ParamTun = luigi.Parameter()

	def run(self):

    		    
	    try:
	        if(self.ParamTun == 'GridSearchCV'):
	            grid_search = GridSearchCV(clf, parameter_values, cv=cv)
	            start = time()
	            y_pred_probs = grid_search.fit(self.X_train, self.y_train).predict_proba(self.X_test)[:,1]
	            y_score = grid_search.fit(self.X_train, self.y_train).decision_function(self.X_test)
	            parameters = grid_search.get_params
	            logger.debug(precision_at_k(self.y_test,y_pred_probs,.05))
	            logger.debug(parameters)
	            logger.debug("grid_search took %.2f seconds" % (time() - start))
	            #print("grid_search took %.2f seconds" % (time() - start))
	            #print(precision_at_k(y_test,y_pred_probs,.05))
	            print(parameters)
	            #plot_precision_recall_n(y_test,y_pred_probs,clf)
	            #plot_roc(y_test,y_score,clf)
	        else:
	            start = time()
	            random_search = RandomizedSearchCV(self.clf, parameter_values)
	            y_pred_probs = random_search.fit(X_train, y_train).predict_proba(X_test)[:,1]
	            parameters = grid_search.get_params
	            #logger.debug(precision_at_k(y_test,y_pred_probs,.05))
	            logger.debug(parameters)
	            logger.debug("RandomizedSearchCV took %.2f seconds" % (time() - start))
	            #print("RandomizedSearchCV took %.2f seconds" % (time() - start))
	            #print(precision_at_k(y_test,y_pred_probs,.05))
	            print(parameters)
	            #plot_precision_recall_n(y_test,y_pred_probs,clf)   
	    except IndexError as e:
	        print('Error:', e)
	        

	    return True 




