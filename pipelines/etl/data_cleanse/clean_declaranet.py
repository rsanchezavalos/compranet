#!/usr/bin/env python 
# -*- coding: utf-8 -*-

"""
Script que limpia la tabla de declaranet. 
Requiere la tabla de declaranet en s3://*/raw

"""

import numpy as np
import pandas as pd
import re

data_path = 'data/declaranet.csv'
data = pd.read_csv(data_path, delimiter = '|', error_bad_lines = False)

def fill_with_near(data):
	data = data.replace(r'^\s*$', np.nan, regex = True) \
	.apply(lambda x: x.str.strip())
	data.loc[:, data.columns != 'SECTOR'] = data.loc[:, data.columns != 'SECTOR'].replace(np.nan, '')
	indexes = data['SECTOR'].index[data['SECTOR'].notnull()]
	d0 = indexes[0]	
	name_rows = data.iloc[data.index[indexes], :]
	for i in range(len(indexes)):
		low_index = indexes[i] - d0
		high_index = indexes[i] + d0
		#Hack para que no truene el último paso
		if i == len(indexes)-1:
			d0 = 0
		else:
			d0 = indexes[i+1] - (indexes[i] + d0)
		row_indexes = list(range(low_index, high_index + 1))
		for col in range(1, len(data.columns)):
			joint_col = data.loc[row_indexes, data.columns[col]].str.cat(sep = ' ')
			name_rows.loc[indexes[i], data.columns[col]] = joint_col
	name_rows = name_rows.apply(lambda x: x.str.strip())
	return(name_rows)