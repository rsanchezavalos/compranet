#! /bin/bash
#### Description: Ingestion Directorio de Funcionarios públicos
###############

echo "Descarga de Directorio Funcionarios Públicos"
wget -q -O- --no-check-certificate 'http://portaltransparencia.gob.mx/pot/repoServlet?archivo=directorioPot.zip'| \
	zcat |  sed -E 's/(^\=|",\=")/,/g;s/("|^ | $|^\,)//g;s/\s+/ /g;s/^\,//g;s/,$//g;' | sed -n '1!p' | 	\
	sed '1s/.*/institucion,nombre,primer_apellido,segundo_apellido,telefono,tipo_personal,cargo,cargo_superior,unidad_administrativa,clave_puesto,nombre_puesto,vacancia,telefono_directo,conmutador,extension,fax,email/g' |\
	sed 's/\,/\|/g'> \
	../../data/funcionarios.csv 
	