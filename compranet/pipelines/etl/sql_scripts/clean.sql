-- Script para crear los foreign keys necesarios para juntar compranet - funcionarios - unidades compradoras.

-- Set UP
-- CREATE EXTENSION  pg_trgm;
-- CREATE EXTENSION fuzzystrmatch;
-- SELECT show_limit();
-- SELECT set_limit(0.9); 

-----------
-- CREA DICCIONARIOS DEPENDENCIA
--- Fuzzy Matching 
-----------

---- FUNCIONARIOS (CORTE EN T)

-- crea ID institucion
DROP TABLE IF EXISTS clean.diccionario_dependencias;
CREATE TABLE clean.diccionario_dependencias AS
    (SELECT distinct on (id_dep_ent || clave_cnet30 || clave_uc) 
        id_dep_ent AS id_institucion_uc,  dependencia_entidad AS institucion_uc, clave_uc, nombre_uc from raw.unidades_compradoras);
 
alter table clean.diccionario_dependencias add institucion_funcionarios TEXT;
 
update clean.diccionario_dependencias AS D
    set institucion_funcionarios = C.institucion_funcionarios 

        FROM (SELECT A.institucion_uc as institucion_uc,
                B.institucion as institucion_funcionarios   
                FROM clean.diccionario_dependencias AS A 

                JOIN (select distinct(institucion) from raw.funcionarios 
                    WHERE institucion IS NOT NULL ) as B

                    ON LEVENSHTEIN(regexp_replace(lower(A.institucion_uc), '[^a-z0-9\s]', '','gi'),
                    regexp_replace(lower(B.institucion), '[^a-z0-9\s]', '','gi'))  <= 5) 

                AS C WHERE  D.institucion_uc = C.institucion_uc;

 
 
CREATE INDEX  IF NOT EXISTS institucion_funcionarios_index ON clean.diccionario_dependencias (institucion_funcionarios);
CREATE INDEX  IF NOT EXISTS institucion_index ON raw.funcionarios (institucion);


-- crea ID CV
DROP TABLE IF EXISTS clean.diccionario_uc ;
CREATE TABLE clean.diccionario_uc AS (select * FROM clean.diccionario_dependencias AS A  WHERE A.institucion_funcionarios is not null);
 
CREATE INDEX  IF NOT EXISTS institucion_funcionarios_index ON clean.diccionario_uc (institucion_funcionarios);
 
ALTER TABLE clean.diccionario_dependencias add uc_funcionarios TEXT;

update clean.diccionario_dependencias AS D
    set uc_funcionarios = C.uc_funcionarios 
    FROM
        (SELECT B.institucion as institucion_funcionarios, B.unidad_administrativa AS  uc_funcionarios,
                A.institucion_uc as institucion_uc, A.nombre_uc AS nombre_uc               
                    FROM clean.diccionario_uc AS A 

                JOIN (select distinct(institucion || unidad_administrativa), 
                            institucion, unidad_administrativa from raw.funcionarios 
                            WHERE unidad_administrativa IS NOT NULL ) as B

                     ON LEVENSHTEIN(regexp_replace(lower(A.nombre_uc), '[^a-z0-9\s]|\#.*|.*\-', '','gi'),
                        regexp_replace(lower(B.unidad_administrativa), '[^a-z0-9\s]', '','gi'))  <= 3
                    AND A.institucion_funcionarios = B.institucion) AS C 

    WHERE  D.institucion_uc = C.institucion_uc AND D.nombre_uc = C.nombre_uc;
 

-- SELECT institucion_uc, institucion_funcionarios, nombre_uc, uc_funcionarios  FROM clean.diccionario_dependencias where uc_funcionarios IS NOT NULL;


-----------------------------------------------------------
-----------------------------------------------------------
-----------------------------------------------------------
---- DECLARANET (HISTÓRICO)
 
-- alter table clean.diccionario_dependencias DROP COLUMN institucion_declaranet;
alter table clean.diccionario_dependencias add institucion_declaranet TEXT;
 
CREATE INDEX  IF NOT EXISTS institucion_declaranet_index ON raw.declaranet (institucion_o_empresa);
CREATE INDEX  IF NOT EXISTS uc_declaranet_index ON raw.declaranet (unidad_administrativa);


-- crea ID institucion
update clean.diccionario_dependencias AS D

    set institucion_declaranet = C.institucion_o_empresa 
        FROM (SELECT A.institucion_uc as institucion_uc,
                    B.institucion_o_empresa as institucion_o_empresa   
                    FROM ( select * from clean.diccionario_dependencias WHERE institucion_uc is not null) AS A 

        JOIN (select distinct on (institucion_o_empresa) institucion_o_empresa from raw.declaranet) as B
             
             ON LEVENSHTEIN(regexp_replace(lower(A.institucion_uc), '[^a-z0-9\s]|\#.*$|^.*\-', '','gi'),
                regexp_replace(lower(substring(B.institucion_o_empresa,1,100)), '[^a-z0-9\s]', '','gi'))  <= 5) AS C 
        
        WHERE  D.institucion_uc = C.institucion_uc;


CREATE INDEX  IF NOT EXISTS institucion_declaranet_index ON clean.diccionario_dependencias (institucion_declaranet);
 
-- SELECT institucion_uc, institucion_funcionarios, institucion_declaranet  FROM clean.diccionario_dependencias where institucion_declaranet IS NOT NULL;

-- Crea id Unidad Compradora




ALTER TABLE clean.diccionario_dependencias DROP COLUMN uc_declaranet;
ALTER TABLE clean.diccionario_dependencias add uc_declaranet TEXT;


update clean.diccionario_dependencias AS D

    set uc_declaranet = C.unidad_administrativa

    FROM

        (SELECT A.nombre_uc AS nombre_uc,

            A.institucion_declaranet as institucion_declaranet, 
            A.clave_uc AS clave_uc,
            B.institucion_o_empresa AS institucion_o_empresa,
            B.unidad_administrativa as unidad_administrativa

                    FROM ( select uc_funcionarios, nombre_uc, institucion_declaranet, clave_uc FROM clean.diccionario_dependencias WHERE institucion_declaranet IS NOT NULL ) as A
                    JOIN ( select institucion_o_empresa, unidad_administrativa from raw.declaranet WHERE unidad_administrativa IS NOT NULL) as B

                         ON LEVENSHTEIN(regexp_replace(lower(A.uc_funcionarios), '[^a-z0-9\s]|\#.*$|^.*\-', '','gi'),
                            regexp_replace(lower(B.unidad_administrativa), '[^a-z0-9\s]', '','gi'))  <= 1 

                        AND A.institucion_declaranet = B.institucion_o_empresa) AS C 

        WHERE D.institucion_declaranet = C.institucion_declaranet


-- SELECT institucion_uc, institucion_funcionarios, institucion_declaranet, uc_declaranet, nombre_uc  FROM clean.diccionario_dependencias where uc_declaranet IS NOT NULL;



-- HACE FALTA LIMPIAR COMPRANET