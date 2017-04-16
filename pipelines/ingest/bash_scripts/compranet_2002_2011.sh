#! /bin/bash
###############
# Compranet 2002 a 2011
###############
#wget
#in2csv
#find

echo "Descarga Compranet De 2002 a 2011"

# Create temporal directory
mkdir ../data/compranet_2002_2011
# Descargar

wget --no-check-certificate http://compranetinfo.funcionpublica.gob.mx/descargas/cnet3/EX{2002..2011}.xlsx -P \
 ../data/compranet_2002_2011 
wget --no-check-certificate http://compranetinfo.funcionpublica.gob.mx/descargas/cnet3/LP{2002..2011}.xlsx -P \
 ../data/compranet_2002_2011 


for filename in ../data/compranet_2002_2011/*.xlsx;
do	in2csv $filename | sed '1d'  >> ../data/compranet_2002_2011/2002_2011.csv; done

cat ../data/compranet_2002_2011/2002_2011.csv | sed -e ':a;s/^\(\("[^"]*"\|'\''[^'\'']*'\''\|[^",'\'']*\)*\),/\1\|/;ta' | \
 sed '1s/.*/DEPENDENCIA_ENTIDAD|NOMBRE_UC|CLAVE_UC|NUMERO_DE_PROCEDIMIENTO|TIPO_DE_PROCEDIMIENTO|TIPO_CONTRATACION|CARACTER|NUMERO_DE_CONTRATO|REFERENCIA_DE_LA_CONTRATACION| FECHA_DE_SUSCRIPCION_DE_CONTRATO|IMPORTE_MN_SIN_IVA|RAZON_SOCIAL|URL_DEL_CONTRATO/g' >\
 ../data/compranet_2002_2011.csv  && rm ../data/compranet_2002_2011/EX* ../data/compranet_2002_2011/LP* \
 ../data/compranet_2002_2011/2002_2011.csv

echo "Deleted temp working directory"
rm -rf ../data/compranet_2002_2011