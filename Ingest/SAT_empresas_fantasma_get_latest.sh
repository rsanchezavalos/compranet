#! /bin/bash
#### Description: Ingestion de datos de empresas fantasma
# Descarga inicial de tablas de contribuyentes con operaciones inexistentes 

###############
# Descarga de datos del SAT
###############

echo 'Descarga de datos de contribuyentes bajo investigación en el SAT'

wget -O- http://www.sat.gob.mx/informacion_fiscal/Paginas/notificacion_contribuyentes_operaciones_inexistentes.aspx | \
grep -E -i -o 'title="Anexo.*" href="\/informacion_fiscal\/Documents\/anexo.*\.pdf' | \
grep -E -i -o 'Documents\/anex.*\.pdf' > anexos.txt

wget -B http://www.sat.gob.mx/informacion_fiscal/ -i anexos.txt -nc -P /tmp/contribuyentes

rm anexos.txt

