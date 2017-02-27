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

# Descargar
wget --no-check-certificate http://compranetinfo.funcionpublica.gob.mx/descargas/cnet3/EX{2002..2011}.xlsx
wget --no-check-certificate http://compranetinfo.funcionpublica.gob.mx/descargas/cnet3/LP{2002..2011}.xlsx

# De 2002 a 2011
for filename in $(ls *.xlsx)
	in2csv $filename | sed '1d' >> 2012_2017.csv

cat 2012_2017.csv | sed '1s/.*/DEPENDENCIA_ENTIDAD,NOMBRE_UC,CLAVE_UC,NUMERO_DE_PROCEDIMIENTO,TIPO_DE_PROCEDIMIENTO,TIPO_CONTRATACION,CARACTER,NUMERO_DE_CONTRATO,REFERENCIA_DE_LA_CONTRATACION, FECHA_DE_SUSCRIPCION_DE_CONTRATO,IMPORTE_MN_SIN_IVA,RAZON_SOCIAL,URL_DEL_CONTRATO/g' | \
	csvsql --db sqlite:///raw.db --insert --table compranet_2002_2011



# De 2010 a 2017

unzip Contratos2010_2012.zip
xlsx2csv Contratos2010_2012_160930120647.xlsx > Contratos2010_2012.csv

unzip Contratos2013.zip
xlsx2csv Contratos2013_170220083907.xlsx > Contratos2013.csv

unzip Contratos2014.zip
xlsx2csv Contratos2014_170220083311.xlsx > Contratos2014.csv

unzip Contratos2015.zip
xlsx2csv Contratos2015_170220082325.xlsx > Contratos2015.csv

unzip Contratos2016.zip
xlsx2csv Contratos2016_170220070535.xlsx > Contratos2016.csv

unzip Contratos2017.zip
xlsx2csv Contratos2017_170220070009.xlsx > Contratos2017.csv

csvstack Contratos2010_2012.csv Contratos2013.csv Contratos2014.csv Contratos2015.csv Contratos2016.csv Contratos217.csv> 2012_2017.csv 

csvsql --db sqlite:///raw.db --table compranet_2012_2017 --insert 2012_2017.csv





