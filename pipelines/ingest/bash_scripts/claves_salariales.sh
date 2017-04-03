###############
# Claves salariales para discriminación de funcionarios
###############

echo "Descarga de Tabla de Remuneraciones en la APF"

wget -q -O-  'http://portaltransparencia.gob.mx/pot/repoServlet?archivo=puestoAPF.zip'| \
zcat| sed -E 's/(^\=|",\=")/,/g;s/("|^ | $|^\,)//g;s/\s+/ /g;s/^\,//g;s/,$//g;'| sed -n '1!p' | \
csvcut -c 1,2,3,7| \
sed '1s/.*/institucion,clave_puesto,nombre_puesto,sueldo_puesto/g'| \
csvgrep -c nombre_puesto_tab -r 'DIRECTOR GENERAL|SECRETARIO|CONTRALOR|TITULAR' | \
PGOPTIONS="--search_path=raw" csvsql --db postgresql://compranet:compranetitam@compranetdb.cwioodotgi4s.us-west-2.rds.amazonaws.com/compranetdb --insert --table claves_salariales 

###############
# Versión alternativa
###############

# wget -q -O temp.zip 'http://portaltransparencia.gob.mx/pot/repoServlet?archivo=puestoAPF.zip'

# unzip -p temp.zip | gsed -E 's/(^\=|",\=")/,/g;s/("|^ | $|^\,)//g;s/\s+/ /g;s/^\,//g;s/,$//g;'| \
# sed -n '1!p' | \
# csvcut -c 1,2,3,7 | \
# sed '1s/.*/institucion,clave_puesto,nombre_puesto_tab,sueldo_puesto/g'| \
# PGOPTIONS="--search_path=raw" csvsql --db postgresql://compranet:compranetitam@compranetdb.cwioodotgi4s.us-west-2.rds.amazonaws.com/compranetdb --insert --table claves_salariales 

###############
# Review de sed
###############

# - 's/(^\=|",\=")/,/g' sustituye globalmente UN '=' o ',=' por ','
# - 's/("|^ | $|^\,)//g' sustituye globalmente UN '"' o ' ' (al principio) o ' ' (al final) por ''
# - 's/\s+/ /g' sustituye globalmente cualquier caracter de espacio (UNO O MÁS tabs, espacios, etc.) por ' '
# - 's/^\,//g;' sustituye globalmente UN ',' al inicio de la línea por ''
# - 's/,$//g' sustituye globalmente UN ',' al final de la línea por ''