###############
# Catálogo de Unidades Compradoras
###############

echo "Descarga Catálogo de Unidades Compradoras"
wget --no-check-certificate  'http://upcp.funcionpublica.gob.mx/descargas/UC.zip' -P $1/ &&\
 unzip ../data/temp/UC.zip -d $1/ && rm $1/UC.zip &&  ls $1/*.xlsx | parallel ssconvert \
 -T Gnumeric_stf:stf_csv {} -L $1/ $1/unidades_compradoras.csv \;  && rm $1/*.xlsx 
