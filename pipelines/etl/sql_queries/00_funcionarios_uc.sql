# Padrón de funcionarios
create table raw.padron_funcionarios as
select nombre_completo
from (select * 
from (select count(*) as cuenta, concat(nombre, primer_apellido, segundo_apellido) as nombre_completo
from raw.funcionarios
group by nombre_completo) as prueba
where cuenta = 1) as filtro;

alter table raw.padron_funcionarios
add id serial primary key;

# Tabla diccionario
# Esto limpia la variable de UC al crear la tabla de diccionario. 
# Creo que falta separar la limpieza de la creación de la tabla,
# y así crear la 
create table clean.diccionario as
select regexp_replace(cast(nombre_uc as text), 'DIRECCION', 'DIRECCIÓN') from
(select regexp_matches(upper("NOMBRE_UC"), '-(.*)\ #.*')
as nombre_uc, "CLAVE_UC" as clave_uc
from raw.unidades_compradoras 
where "DEPENDENCIA_ENTIDAD" ~ 'Secretaría') as subq
where cast(nombre_uc as text) ~* 'Dirección General';

# Limpia UAs 
select distinct unidad_administrativa
from (select regexp_replace(unidad_administrativa, 'DIRECCION', 'DIRECCIÓN') as unidad_administrativa
from raw.funcionarios 
where institucion ~ 'SECRETARÍA' or institucion ~ 'SECRETARIA') as unidades_clean 
where unidad_administrativa ~* 'Dirección General';

# Pendientes: incluir el resto de las UA/UCs que coincidan con ciertas claves salariales

