#! /bin/bash
#### Descripción: Tarea Grupal 1  
# Integrantes:
# Thalía Guerra
# Roberto Sánchez 
# Mónica Zamudio 
# Manuel Aragones

echo "Descargando Archivos de Gdelt Project"
mkdir temp_gdelt
#El URL de descarga de eventos de [[http://gdeltproject.org/][=GDELT=]] es
#- Descarguen los archivos desde el mes de Diciembre de 2016 (usando =parallel)
http http://data.gdeltproject.org/events/index.html | grep -oP '201(612|7)[0-9]*\.export.CSV.zip' | \
awk '{print "http://data.gdeltproject.org/events/"$0}' | uniq | parallel wget -P ./temp_gdelt/


# Peso los archivos comprimidos
$( echo 'peso de archivos' `du -h .` ) 
# Número de archivos
$( echo 'numero de archivos: '`ls *.zip | wc -l` )


#- Usando =parallel= y sin descomprimir los archivos guarda los registros de
#  México en una tabla =mexico= en una base de datos =sqlite= llamada =gdelt.db=
wget -nc http://gdeltproject.org/data/lookups/CSV.header.dailyupdates.txt -O temp.csv

ls *.CSV.zip | parallel -j0 zgrep -e "MEXICO"  | cat  | csvsql --db sqlite:///gdelt.db --table mexico --insert -t 

#- Al comando anterior agrega =tee= y guarda en otra *tabla* (llamada mexico_ts=) el 
# número de eventos por día y la escala de goldstein 

sqlite3 gdelt.db "CREATE TABLE mexico_ts AS SELECT DATEADDED,COUNT(DATEADDED), avg(GoldsteinScale) FROM mexico where Actor1CountryCode="MEX" or Actor2CountryCode="MEX" GROUP BY DATEADDED;" 