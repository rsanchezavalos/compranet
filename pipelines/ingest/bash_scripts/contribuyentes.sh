#! /bin/bash
#### Description: Ingestion de datos de empresas fantasma
# Descarga inicial de tablas de contribuyentes con operaciones inexistentes 

###############
# Descarga de datos del SAT
###############

echo 'Descarga de datos de contribuyentes bajo investigación en el SAT'

wget -O- http://www.sat.gob.mx/informacion_fiscal/Paginas/notificacion_contribuyentes_operaciones_inexistentes.aspx > prueba.txt | \
grep -E -i -o 'title="Anexo\ [0-9]+\ del\ oficio\ [0-9]+" href="\/informacion_fiscal\/Documents\/anexo.*\.pdf' | \
grep -E -i -o 'Documents\/anexo.*\.pdf' > anexos.txt

[ -d /tmp/contribuyentes ] || wget -B http://www.sat.gob.mx/informacion_fiscal/ -i anexos.txt -P /tmp/contribuyentes

rm anexos.txt