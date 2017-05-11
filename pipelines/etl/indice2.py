import pandas as pd
import numpy as np

data = pd.DataFrame.from_csv('/home/thalia/Escritorio/Compranet/base_final_v3.csv')

variables_comprador = 'ANUNCIO', 'PROVEEDOR_CONTRATISTA', 'FOLIO_RUPC', 'TITULO_CONTRATO'

variables_proveedor = 'ANUNCIO', 'FOLIO_RUPC', 'TITULO_EXPEDIENTE'

indice_dependencia = 0

indice_unidad_compradora = 0

indice_proveedor = 0

for variable in variables_comprador:
    tabla = pd.crosstab(data.DEPENDENCIA, pd.isnull(data[variable]))
    promedio_columnas = tabla.mean(axis = 0)
    promedio = tabla[1]/promedio_columnas[1]
    total_filas = tabla.sum(axis = 1)
    total_obs = total_filas.sum()
    ponderador = total_obs/total_filas
    suma += promedio*ponderador

media = suma.mean
sd = suma.np.std
indice_dependencia = (suma - media)/sd
    
for variable in variables_comprador:
    tabla = pd.crosstab(data.NOMBRE_DE_LA_UC, pd.isnull(data[variable]))
    promedio_columnas = tabla.mean(axis = 0)
    promedio = tabla[1]/promedio_columnas[1]
    total_filas = tabla.sum(axis = 1)
    total_obs = total_filas.sum()
    ponderador = total_obs/total_filas
    suma += promedio*ponderador

media = suma.mean
sd = suma.np.std
indice_unidad_compradora = (suma - media)/sd
    
    
for variable in variables_proveedor:
    tabla = pd.crosstab(data.PROVEEDOR_CONTRATISTA, pd.isnull(data[variable]))
    promedio_columnas = tabla.mean(axis = 0)
    promedio = tabla[1]/promedio_columnas[1]
    total_filas = tabla.sum(axis = 1)
    total_obs = total_filas.sum()
    ponderador = total_obs/total_filas
    suma += promedio*ponderador
    
media = suma.mean
sd = suma.np.std
indice_proveedor = (suma - media)/sd

