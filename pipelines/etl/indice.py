import pandas as pd
import numpy as np

data = pd.DataFrame.from_csv('/home/thalia/Escritorio/Compranet/base_final_v3.csv')

variables_comprador = 'ANUNCIO', 'ORGANISMO', 'C_EXTERNO', 'ESTRATIFICACION_MPC', 'PROVEEDOR_CONTRATISTA', 'FOLIO_RUPC', 'ESTRATIFICACION_MUC', 'CLAVE_CARTERA_SHCP', 'PLURIANUAL', 'COMPRA_CONSOLIDADA', 'IDENTIFICADOR_CM', 'CONTRATO_MARCO', 'FECHA_CELEBRACION', 'APORTACION_FEDERAL', 'CLAVE_PROGRAMA', 'RAMO', 'TITULO_CONTRATO', 'FORMA_PROCEDIMIENTO', 'TIPO_PROCEDIMIENTO', 'CARACTER', 'FECHA_APERTURA_PROPOSICIONES', 'PROC_F_PUBLICACION', 'EXP_F_FALLO', 'NUMERO_PROCEDIMIENTO', 'PLANTILLA_EXPEDIENTE', 'TITULO_EXPEDIENTE'

variables_proveedor = 'ANUNCIO', 'ORGANISMO', 'C_EXTERNO', 'ESTRATIFICACION_MPC', 'FOLIO_RUPC', 'ESTRATIFICACION_MUC', 'CLAVE_CARTERA_SHCP', 'PLURIANUAL', 'COMPRA_CONSOLIDADA', 'IDENTIFICADOR_CM', 'CONTRATO_MARCO', 'FECHA_CELEBRACION', 'APORTACION_FEDERAL', 'CLAVE_PROGRAMA', 'RAMO', 'TITULO_CONTRATO', 'FORMA_PROCEDIMIENTO', 'TIPO_PROCEDIMIENTO', 'CARACTER', 'FECHA_APERTURA_PROPOSICIONES', 'PROC_F_PUBLICACION', 'EXP_F_FALLO', 'NUMERO_PROCEDIMIENTO', 'PLANTILLA_EXPEDIENTE', 'TITULO_EXPEDIENTE'

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

