#! /bin/bash
#### Descripción: Tarea Grupal 1  
# Integrantes:
# Thalía Guerra
# Roberto Sánchez 
# Mónica Zamudio 
# Manuel Aragones

echo "Descargando Archivos de Gdelt Project"
mkdir temp_gdelt

#- Descarguen los archivos desde el mes de Diciembre de 2016 (usando =parallel)
http http://data.gdeltproject.org/events/index.html | grep -oP '201(612|7)[0-9]*\.export.CSV.zip' | \
awk '{print "http://data.gdeltproject.org/events/"$0}' | uniq | parallel wget -P ./temp_gdelt/

# Peso los archivos comprimidos;  Número de archivos
echo 'peso de archivos' `du -h ./temp_gdelt`; echo 'numero de archivos: '`ls ./temp_gdelt/*.zip | wc -l`;

#- Usando =parallel= y sin descomprimir los archivos guarda los registros de en una tabla =mexico=
header=$( wget -qO- http://gdeltproject.org/data/lookups/CSV.header.dailyupdates.txt | sed -E 's/[[:space:]]+/|/g' )
ls ./temp_gdelt/*.CSV.zip | parallel -j0 zgrep -e "MEXICO" >> temp.csv  
cat temp.csv | sed "1s/.*/$header/g" | csvsql --db sqlite:///gdelt.db --table mexico --insert -t 

#- Al comando anterior agrega =tee= y guarda en otra *tabla* (llamada mexico_ts=) con número de eventos por día y la escala de goldstein 
cat temp.csv | sed "1s/.*/$header/g" | csvsql --db sqlite:///gdelt.db --table mexico --insert -t 
sqlite3 gdelt.db  'CREATE TABLE mexico_ts AS SELECT DATEADDED,COUNT(DATEADDED), avg(GoldsteinScale) FROM mexico where Actor1CountryCode="MEX" or Actor2CountryCode="MEX"  GROUP BY DATEADDED;'



