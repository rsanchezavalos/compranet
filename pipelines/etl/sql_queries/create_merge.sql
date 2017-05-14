# Script que junta tablas de compranet con funcionarios.

# Crear la tabla de UA-UC con institución, unidad_administrativa, nombre_uc

create table clean.diccionario_unidades(
	institucion varchar(100),
	unidad_administrativa varchar(100),
	nombre_uc varchar(100)
)

##### Comparar y escribir sobre la tabla nueva  #########

# Pseudocode: 
# Agrupando por dependencia, condicionando a 2017:
# Para cada nombre_ua de funcionarios, compararlo con todos los nombres distintos de nombre_uc en Compranet.
# Escribirlos como renglón sólo si sus soundex son similares

# Dadas institución, UA, buscar entre UCs

CREATE OR REPLACE FUNCTION compare_insert (ua VARCHAR(100), inst VARCHAR(100))
RETURNS VOID AS $$ 

BEGIN

FOR * IN SELECT DISTINCT nombre_uc FROM clean.compranet WHERE dependencia ~* inst 
	LOOP
	IF difference(ua, *) > 2 THEN 
		INSERT INTO diccionario_unidades (institucion, unidad_administrativa, nombre_uc)
		    VALUES (inst, ua, *);
	END IF;
END LOOP;

END ; 
$$ LANGUAGE plpgsql;


## Loop sobre UAs, dada una institución

CREATE OR REPLACE FUNCTION find_ua (inst varchar(100))
RETURNS VOID AS $$

BEGIN

FOR * IN SELECT DISTINCT unidad_administrativa WHERE institucion == inst 
	LOOP
		compare_insert(*, inst)
	END LOOP;

END ;
$$ LANGUAGE plpgsql

