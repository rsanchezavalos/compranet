#! /bin/bash
###############
# Compranet 2002 a 2011
###############
#wget
#unzip
#parallel
#ssconvert
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


###############
# Compranet 2010 a 2016
###############


echo "Descarga Compranet De 2010 a 2016"

# Create temporal directory
mkdir ../data/compranet_2010_2016

# Download Historic
wget --no-check-certificate  https://compranetinfo.funcionpublica.gob.mx/descargas/cnet/Contratos2010_2012.zip -P \
	../data/compranet_2010_2016
wget --no-check-certificate  https://upcp.funcionpublica.gob.mx/descargas/Contratos{2013..2016}.zip -P \
	../data/compranet_2010_2016

for f in $( ls ../data/compranet_2010_2016/*.zip ); do unzip "$f" -d ../data/compranet_2010_2016; done; 
rm ../data/compranet_2010_2016/*.zip

find ../data/compranet_2010_2016 -name '*.xlsx' | ssconvert -D ../data/compranet_2010_2016/ -T Gnumeric_stf:stf_csv {} \; \
 && rm ../data/compranet_2010_2016/*.xlsx

cat $( find ../data/compranet_2010_2016 -name '*.csv' ) | sed '1d' | sed -e ':a;s/^\(\("[^"]*"\|'\''[^'\'']*'\''\|[^",'\'']*\)*\),/\1\t/;ta' | \
	sed 's/\t/|/g'  >> ../data/compranet_2010_2016/2010_2016.csv

cat ../data/compranet_2010_2016/2010_2016.csv | sed '1s/.*/GOBIERNO|SIGLAS|DEPENDENCIA|CLAVE_UC|NOMBRE_DE_LA_UC|RESPONSABLE|CODIGO_EXPEDIENTE|TITULO_EXPEDIENTE|PLANTILLA_EXPEDIENTE|NUMERO_PROCEDIMIENTO|EXP_F_FALLO|PROC_F_PUBLICACION|FECHA_APERTURA_PROPOSICIONES|CARACTER|TIPO_CONTRATACION|TIPO_PROCEDIMIENTO|FORMA_PROCEDIMIENTO|CODIGO_CONTRATO|TITULO_CONTRATO|FECHA_INICIO|FECHA_FIN|IMPORTE_CONTRATO|MONEDA|ESTATUS_CONTRATO|ARCHIVADO|CONVENIO_MODIFICATORIO|RAMO|CLAVE_PROGRAMA|APORTACION_FEDERAL|FECHA_CELEBRACION|CONTRATO_MARCO|IDENTIFICADOR_CM|COMPRA_CONSOLIDADA|PLURIANUAL|CLAVE_CARTERA_SHCP|ESTRATIFICACION_MUC|FOLIO_RUPC|PROVEEDOR_CONTRATISTA|ESTRATIFICACION_MPC|SIGLAS_PAIS|ESTATUS_EMPRESA|CUENTA_ADMINISTRADA_POR|C_EXTERNO|ORGANISMO|ANUNCIO/g' > ../data/compranet_2010_2016.csv

rm -rf ../data/compranet_2010_2016
echo "Deleted temp working directory compranet_2010_2016"

# # register the cleanup function to be called on the EXIT signal
trap cleanup EXIT