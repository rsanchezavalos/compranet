###############
# Catálogo de Unidades Compradoras
###############

# Create temporal directory
mkdir ../data/unidades_compradoras

echo "Descarga Catálogo de Unidades Compradoras"
wget --no-check-certificate  'http://upcp.funcionpublica.gob.mx/descargas/UC.zip' -P ../data/unidades_compradoras
unzip ../data/unidades_compradoras/UC.zip -d ../data/unidades_compradoras && rm ../data/unidades_compradoras/UC.zip 
find ../data/unidades_compradoras/*.xlsx | ssconvert -T Gnumeric_stf:stf_csv ../data/unidades_compradoras/*.xlsx \
  -L ../data/unidades_compradoras/ ../data/unidades_compradoras.csv 
rm ../data/unidades_compradoras/*.xlsx 

function cleanup {      
  rm -rf ../data/unidades_compradoras
  echo "Deleted temp working directory ../data/unidades_compradoras"
}

# register the cleanup function to be called on the EXIT signal
trap cleanup EXIT