#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import re
import math


def fill_with_near(data):
    """strip()
    Script que limpia la tabla de declaranet. 
    Requiere la tabla de declaranet en s3://*/raw

    """

    # Limpieza
    data = data.astype(str)
    #data = data.apply(lambda x: x.str.strip())
    data = data.replace(r'nan', np.nan, regex=True)
    #data = data.dropna(axis=0, how='all',subset={'SECTOR', 'PODER', 'AMBITO', 'INSTITUCION_O_EMPRESA','UNIDAD_ADMINISTRATIVA', 'PUESTO', 'FUNCION_PRINCIPAL','INGRESO_EGRESO'})
    #data.loc[:, data.columns != 'INGRESO_EGRESO'] = data.loc[:, data.columns != 'SECTOR'].replace(np.nan, '')
    data.reset_index(inplace=True)

    # Construcción Base de datos Padre
    indexes = data['INGRESO_EGRESO'].index[data['INGRESO_EGRESO'].notnull()]
    name_rows = data.iloc[data.index[indexes], :]

    data["group"] = np.nan
    d_1 = indexes[0]

    for i in range(len(indexes)):
        print(i)

        if i == len(indexes)-1:

            # Último grupo
            low_index = math.floor(indexes[i] - d_1)
            high_index = len(data)

        else:

            # Orden de grupos
            low_index = math.floor(indexes[i] - d_1)
            sep_up = (indexes[i+1] - indexes[i])/2
            sep_down = (indexes[i] - low_index)
            sep = max(sep_up, 2)
            sep_M = max(sep_down, 2)
            high_index = math.ceil(indexes[i] + sep)
            d_1 = sep

        row_indexes = list(range(int(low_index), int(high_index)))
        data.iloc[row_indexes, data.columns.get_loc('group')] = i

    #data["INGRESO_EGRESO"][data.INGRESO_EGRESO.isnull()==False] = data["INGRESO_EGRESO"][data.INGRESO_EGRESO.isnull()==False].astype(str)
    #data['INGRESO_EGRESO'] = data['INGRESO_EGRESO'].astype(str)

    names = pd.DataFrame(data.groupby('group')['NOMBRE'].first())
    groups = data.groupby('group')['SECTOR', 'PODER', 'AMBITO', 'INSTITUCION_O_EMPRESA', 'UNIDAD_ADMINISTRATIVA',
      'PUESTO', 'FUNCION_PRINCIPAL', 'INGRESO_EGRESO'].agg(lambda x: ' '.join(x.dropna()).strip().lower())
    name_rows = names.merge(groups, left_index=True, right_index=True)
    name_rows = name_rows.apply(lambda x: x.str.replace("  +"," "))

    del name_rows["group"]

    data[["year_start","year_end"]] = data.INGRESO_EGRESO.str.split("-",expand=True,n=1)
    data['year_start'] = data["year_start"].str.extract(r'(\d{4})').fillna(0).astype(int)
    data['year_end'] = data["year_end"].str.extract(r'(\d{4})').fillna(0).astype(int)    

    return(name_rows)

