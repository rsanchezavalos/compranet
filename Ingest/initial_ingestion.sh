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

echo "Descarga Compranet De 2002 a 2011"
# Descargar
wget --no-check-certificate http://compranetinfo.funcionpublica.gob.mx/descargas/cnet3/EX{2002..2011}.xlsx
wget --no-check-certificate http://compranetinfo.funcionpublica.gob.mx/descargas/cnet3/LP{2002..2011}.xlsx

for filename in $(ls *.xlsx)
	in2csv $filename | sed '1d' >> 2002_2011.csv

cat 2002_2011.csv | sed '1s/.*/DEPENDENCIA_ENTIDAD,NOMBRE_UC,CLAVE_UC,NUMERO_DE_PROCEDIMIENTO,TIPO_DE_PROCEDIMIENTO,TIPO_CONTRATACION,CARACTER,NUMERO_DE_CONTRATO,REFERENCIA_DE_LA_CONTRATACION, FECHA_DE_SUSCRIPCION_DE_CONTRATO,IMPORTE_MN_SIN_IVA,RAZON_SOCIAL,URL_DEL_CONTRATO/g' | \
	csvsql --db sqlite:///raw.db --insert --table compranet_2002_2011
rm EX* LP*


echo "Descarga Compranet De 2010 a 2017"

wget --no-check-certificate  https://compranetinfo.funcionpublica.gob.mx/descargas/cnet/Contratos2010_2012.zip 
wget --no-check-certificate  https://upcp.funcionpublica.gob.mx/descargas/Contratos{2013..2017}.zip 
for f (./*.zip) unzip $f 
rm *.zip
find . -name '*.xlsx' | parallel ssconvert -T Gnumeric_stf:stf_csv {} \;
rm *.xlsx


#csvstack > 2012_2017.csv 
#csvsql --db sqlite:///raw.db --table compranet_2012_2017 --insert 2012_2017.csv





