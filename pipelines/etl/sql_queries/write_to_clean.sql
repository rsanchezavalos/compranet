# Limpia tablas de funcionarios y compranet 

# Tabla de compranet
create table clean.compranet as
select regexp_matches(upper(nombre_de_la_uc), '.*-(.*)\ #.*')
as nombre_uc, 
claveuc as clave_uc,
dependencia as dependencia,
responsable as responsable,
numero_procedimiento as numero_procedimiento,
tipo_contratacion as tipo_contratacion,
tipo_procedimiento as tipo_procedimiento,
fecha_inicio as fecha_inicio,
fecha_fin as fecha_fin,
importe_contrato as importe_contrato,
clave_cartera_shcp as clave_cartera_shcp,
estratificacion_mpc as estratificacion_mpc,
proveedor_contratista as proveedor_contratista,
folio_rupc as folio_rupc
from raw.compranet

#Tabla de funcionarios
create table clean.funcionarios as
select * from raw.funcionarios;

#NOTA: ¿Será bueno hacer algo distinto con los nombres de esta segunda tabla?