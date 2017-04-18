#! /bin/bash
#### Description: Ingestion de claves salariales
# Descarga inicial de tabla de remuneraciones de funcionarios de la APF 
###############
# Claves salariales para discriminación de funcionarios
###############

echo "Descarga de Tabla de Remuneraciones en la APF"

wget -q -O-  'http://portaltransparencia.gob.mx/pot/repoServlet?archivo=puestoAPF.zip'| \
zcat| sed -E 's/(^\=|",\=")/,/g;s/("|^ | $|^\,)//g;s/\s+/ /g;s/^\,//g;s/,$//g;'| sed -n '1!p' > ../data/claves_salariales.csv