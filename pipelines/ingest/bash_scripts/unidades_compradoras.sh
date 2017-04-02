###############
# Catálogo de Unidades Compradoras
###############

echo "Descarga Catálogo de Unidades Compradoras"
wget --no-check-certificate  'http://upcp.funcionpublica.gob.mx/descargas/UC.zip' -P ../data/temp
unzip ../data/temp/UC.zip -d ../data/temp && rm ../data/temp/UC.zip 
find ../data/temp/*.xlsx | ssconvert -T Gnumeric_stf:stf_csv ../data/temp/*.xlsx   -L ../data/temp/ ../data/temp/unidades_compradoras.csv 
rm ../data/temp/*.xlsx 
