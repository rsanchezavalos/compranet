#!/bin/bash
if [ -d ./tarea_1_b ]; then rm -rf ./tarea_1_b; fi
$( mkdir tarea_1_b ) 

for servicio in $( http http://swapi.co/api/ --check-status --ignore-stdin | jq -r 'keys_unsorted[] | @uri' ); do
	var="$( http http://swapi.co/api/$servicio/  | jq --compact-output -r '.next' )"
	echo "Descargando servicio: "$servicio "- paginación: 1" 
	$( http http://swapi.co/api/$servicio/\?page=1 | jq  --compact-output -r  '.results[]'  | in2csv -f ndjson -v >> ./tarea_1_b/$servicio.csv )
	COUNTER=2
	while [ $var != null ]; do
		echo "Intentando descargar servicio: "$servicio "- paginación: " $COUNTER
		$( http http://swapi.co/api/$servicio/\?page=$COUNTER | jq  --compact-output -r  '.results[]'  | in2csv -f ndjson -v >> ./tarea_1_b/$servicio.csv )
		COUNTER=$[$COUNTER+1]
		var="$( http http://swapi.co/api/$servicio/\?page=$COUNTER  | jq --compact-output -r '.next' )"
	done
	$( cat ./tarea_1_b/$servicio.csv |  csvsql --db sqlite:///star_wars_B.db --insert --table $servicio)
done

 