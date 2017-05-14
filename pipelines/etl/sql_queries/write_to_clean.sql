# Limpia tablas de funcionarios y compranet 

# Tabla de compranet
create table clean.compranet as
select regexp_replace(cast(nombre_uc as text), 'DIRECCION', 'DIRECCIÓN') from
(select regexp_matches(upper("NOMBRE_DE_LA_UC"), '-(.*)\ #.*')
as nombre_uc, 
"CLAVE_UC" as clave_uc,
"DEPENDENCIA" as dependencia,
"RESPONSABLE" as responsable,
"NUMERO_PROCEDIMIENTO" as numero_procedimiento,
"TIPO_CONTRATACION" as tipo_contratacion,
"TIPO_PROCEDIMIENTO" as tipo_procedimiento,
"FECHA_INICIO" as fecha_inicio,
"FECHA_FIN"	as fecha_fin,
"IMPORTE_CONTRATO" as importe_contrato,
"CLAVE_CARTERA_SHCP" as clave_cartera_shcp,
"ESTRATIFICACION_MUC" as estratificacion_muc,
"PROVEEDOR_CONTRATISTA" as proveedor_contratista,
"FOLIO_RUPC" as folio_rupc
from raw.compranet) as subq;

#Tabla de funcionarios
create table clean.funcionarios as
select * from raw.funcionarios;

#NOTA: ¿Será bueno hacer algo distinto con los nombres de esta segunda tabla?