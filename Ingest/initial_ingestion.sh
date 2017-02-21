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

wget --no-check-certificate -i Lista_URL_Compranet.txt

# De 2002 a 2011

in2csv EX2002.xlsx > EX2002.csv
in2csv EX2003.xlsx > EX2003.csv
in2csv EX2004.xlsx > EX2004.csv
in2csv EX2005.xlsx > EX2005.csv
in2csv EX2006.xlsx > EX2006.csv
in2csv EX2007.xlsx > EX2007.csv
in2csv EX2008.xlsx > EX2008.csv
in2csv EX2009.xlsx > EX2009.csv
in2csv EX2010.xlsx > EX2010.csv
in2csv EX2011.xlsx > EX2011.csv

in2csv LP2002.xlsx > LP2002.csv
in2csv LP2003.xlsx > LP2003.csv
in2csv LP2004.xlsx > LP2004.csv
in2csv LP2005.xlsx > LP2005.csv
in2csv LP2006.xlsx > LP2006.csv
in2csv LP2007.xlsx > LP2007.csv
in2csv LP2008.xlsx > LP2008.csv
in2csv LP2009.xlsx > LP2009.csv
in2csv LP2010.xlsx > LP2010.csv
in2csv LP2011.xlsx > LP2011.csv

# Juntar 2002 a 2011

csvstack EX2002.csv EX2003.csv EX2004.csv EX2005.csv EX2006.csv EX2007.csv EX2008.csv EX2009.csv EX2010.csv EX2011.csv LP2002.csv LP2003.csv LP2004.csv LP2005.csv LP2006.csv LP2007.csv LP2008.csv LP2009.csv LP2010.csv LP2011.csv > 2002_2011.csv | csvsql --db sqlite:///raw.db --insert --table compranet_2002_2011

csvsql --db sqlite:///raw.db --table compranet_2002_2011 --insert 2002_2011.csv


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

