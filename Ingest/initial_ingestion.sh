#! /bin/bash
#### Description: Ingestion Bash Script  
# Descarga inicial para exploración de bases de datos para entender el proyecto
# Este código - aún no es parte del pipeline TODO(Luigi)


###############
# Directorio de Funcionarios públicos
echo "Descarga de Directorio Funcionarios Públicos"
wget -q -O-  'http://portaltransparencia.gob.mx/pot/repoServlet?archivo=directorioPot.zip'| \
	zcat |  sed -E 's/(^\=|",\=")/,/g;s/("|^ | $|^\,)//g;s/\s+/ /g;s/^\,//g;s/,$//g;' | sed -n '1!p' | 	\
	sed '1s/.*/institucion,nombre,primer_apellido,segundo_apellido,telefono,tipo_personal,cargo,cargo_superior,unidad_administrativa,clave_puesto,nombre_puesto,vacancia,telefono_directo,conmutador,extension,fax,email/g' | \
	csvsql --db sqlite:///raw.db --insert --table funcionarios 


###############
# Compranet

