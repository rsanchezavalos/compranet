CREATE INDEX  IF NOT EXISTS claveuc_compranet_index ON raw.compranet (claveuc);

-- Funcionario es el corte en t de declaranet
-- A cada funcionario le agregamos el id de clave_uc
-- Merge entre tabla funcionario y tabla diccionario

DROP TABLE IF EXISTS clean.funcionarios;
CREATE TABLE clean.funcionarios AS (select * from raw.funcionarios);

CREATE INDEX  IF NOT EXISTS funcionarios_institucion_index ON clean.funcionarios (institucion);
CREATE INDEX  IF NOT EXISTS funcionarios_unidad_administrativa ON clean.funcionarios (unidad_administrativa);

CREATE INDEX  IF NOT EXISTS dic_inst_fun_index ON clean.diccionario_dependencias (institucion_funcionarios);
CREATE INDEX  IF NOT EXISTS dic_uc_fun_index ON clean.diccionario_dependencias (uc_funcionarios);

ALTER TABLE clean.funcionarios add clave_uc TEXT;



UPDATE clean.funcionarios AS funcionarios
    set  clave_uc = diccionarios.clave_uc 
	    FROM clean.diccionario_dependencias as diccionarios
	    WHERE diccionarios.institucion_funcionarios = funcionarios.institucion
		AND diccionarios.uc_funcionarios = funcionarios.unidad_administrativa


