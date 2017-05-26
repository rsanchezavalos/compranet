import logging
import logging.config
#logging.config.fileConfig('intro-to-ds-logging.conf')
logger = logging.getLogger()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('example.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
logger.addHandler(fh)

import pandas as pd
import numpy as np

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
from sklearn.grid_search import GridSearchCV
from sklearn.grid_search import RandomizedSearchCV
from sklearn.metrics import roc_curve, auc
from sklearn import datasets


import random
import pylab as pl
import matplotlib.pyplot as plt
from scipy import optimize
import time
import feather
import sqlite3
from time import time
import numpy as np

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



def plot_precision_recall_n(y_true, y_prob, model_name):
    from sklearn.metrics import precision_recall_curve
    y_score = y_prob
    precision_curve, recall_curve, pr_thresholds = precision_recall_curve(y_true, y_score)
    precision_curve = precision_curve[:-1]
    recall_curve = recall_curve[:-1]
    pct_above_per_thresh = []
    number_scored = len(y_score)
    for value in pr_thresholds:
        num_above_thresh = len(y_score[y_score>=value])
        pct_above_thresh = num_above_thresh / float(number_scored)
        pct_above_per_thresh.append(pct_above_thresh)
    pct_above_per_thresh = np.array(pct_above_per_thresh)
    plt.clf()
    fig, ax1 = plt.subplots()
    ax1.plot(pct_above_per_thresh, precision_curve, 'b')
    ax1.set_xlabel('percent of population')
    ax1.set_ylabel('precision', color='b')
    ax2 = ax1.twinx()
    ax2.plot(pct_above_per_thresh, recall_curve, 'r')
    ax2.set_ylabel('recall', color='r')
    
    name = model_name
    plt.title(name)
    #plt.savefig(name)
    plt.show()

def plot_roc(y_test, y_score,model_name, n_classes=1, iclass = 0, multi = False):
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.metrics import roc_curve, auc
    fpr = dict()
    tpr = dict()
    roc_auc = dict()
    for i in range(n_classes):
        fpr[i], tpr[i], _ = roc_curve(y_test, y_score)
        roc_auc[i] = auc(fpr[i], tpr[i])

    # Compute micro-average ROC curve and ROC area
    #fpr["micro"], tpr["micro"], _ = roc_curve(y_test.ravel(), y_score.ravel())
    #roc_auc["micro"] = auc(fpr["micro"], tpr["micro"])
    if (multi == False):
        plt.figure()
        lw = 2
        plt.plot(fpr[iclass], tpr[iclass], color='darkorange', lw=lw, label='ROC curve (area = %0.2f)' % roc_auc[iclass])
        plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
        plt.xlim([-0.5, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        name = model_name
        plt.title(name)
        plt.legend(loc="lower right")
        plt.show()
    else:
        colors = cycle(['navy', 'turquoise', 'darkorange', 'cornflowerblue','teal'])
        plt.figure()
        lw = 2
        for j, color in zip(range(n_classes), colors):
            plt.plot(fpr[j], tpr[j], color = color, lw= lw, label='ROC curve (area = %0.2f)' % roc_auc[j])
        plt.plot([0,1],[0,1],'k--', lw=lw)
        plt.xlim([0.0,1.0])
        plt.ylim([0.0,1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        name = model_name
        plt.title(name)
        plt.legend(loc = "lower right")
        name = model_name
        plt.show()
        

def precision_at_k(y_true, y_scores, k):
    threshold = np.sort(y_scores)[::-1][int(k*len(y_scores))]
    y_pred = np.asarray([1 if i >= threshold else 0 for i in y_scores])
    return metrics.precision_score(y_true, y_pred, average = 'micro')


def magic_loop(models_to_run, clfs, grid, X, y, cv = 5,ParamTun = 'GridSearchCV'):
    for n in range(1, 2):
        X_train, X_test, y_train, y_test = train_test_split(X, y)
        for index, clf in enumerate([clfs[x] for x in models_to_run]):
            logger.debug(models_to_run[index])
            print(models_to_run[index])
            parameter_values = grid[models_to_run[index]]
            try:
                if(ParamTun == 'GridSearchCV'):
                    grid_search = GridSearchCV(clf, parameter_values, cv=cv)
                    start = time()
                    y_pred_probs = grid_search.fit(X_train, y_train).predict_proba(X_test)[:,1]
                    y_score = grid_search.fit(X_train, y_train).decision_function(X_test)
                    parameters = grid_search.get_params
                    logger.debug(precision_at_k(y_test,y_pred_probs,.05))
                    logger.debug(parameters)
                    logger.debug("grid_search took %.2f seconds" % (time() - start))
                    #print("grid_search took %.2f seconds" % (time() - start))
                    #print(precision_at_k(y_test,y_pred_probs,.05))
                    print(parameters)
                    #plot_precision_recall_n(y_test,y_pred_probs,clf)
                    #plot_roc(y_test,y_score,clf)
                else:
                    start = time()
                    random_search = RandomizedSearchCV(clf, parameter_values)
                    y_pred_probs = random_search.fit(X_train, y_train).predict_proba(X_test)[:,1]
                    parameters = grid_search.get_params
                    logger.debug(precision_at_k(y_test,y_pred_probs,.05))
                    logger.debug(parameters)
                    logger.debug("RandomizedSearchCV took %.2f seconds" % (time() - start))
                    #print("RandomizedSearchCV took %.2f seconds" % (time() - start))
                    #print(precision_at_k(y_test,y_pred_probs,.05))
                    print(parameters)
                    #plot_precision_recall_n(y_test,y_pred_probs,clf)   
            except IndexError as e:
                print('Error:', e)
                continue


def main(): 
    clfs, grid = define_hyper_params()
    models_to_run_GS=['LR', 'AB']
    models_to_run_RS=['KNN','RF','GB','DT']
    iris = datasets.load_iris()
    encoders = dict()
    X = iris.data
    y = iris.target
    #magic_loop(models_to_run_RS, clfs,grid, X,y, cv = 5, ParamTun = 'RandomSearchCV')
    magic_loop(models_to_run_GS, clfs,grid, X,y, cv = 5, ParamTun = 'GridSearchCV')

if __name__ == '__main__':
    main()