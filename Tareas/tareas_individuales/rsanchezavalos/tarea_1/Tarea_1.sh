#! /bin/bash
#Tarea 1: Individual - rsanchezavalos
echo "Tarea 1: Roberto Sánchez Ávalos"

echo "Empezando Parte A"
# Ejercicio A
#- Mezcla los comandos =httppie=, =jq= y =csvkit= para descargar las películas de *Star Wars* y guardar los campos de   
#  =title,episode_id,director,producer,release_date,opening_crawl= en una base de
#  datos =sqlite= llamada =star_wars.db=.
$( http http://swapi.co/api/films/ | jq -c -r '["title", "episode_id", "director", "producer", "release_date"," opening_crawl"], (.results[] | [.title, .episode_id, .director, .producer, .release_date, .opening_crawl]) | @csv'  | csvsql --db sqlite:///star_wars_A.db --insert --table films )


echo "Empezando Parte B"
# Ejercicio B:
#- Usando =bash= crea un programa que descargue todas los /resources/ de *SWAPI*
#  http GET http://swapi.co/api/
#  y guárdalos en =jsons= separados usando como nombres de archivo la llave del
#  Toma en cuenta la paginación. Al final deberás de tener sólo 7 archivos.
#  Procesa estos archivos con las herramientas del primer inciso de la tarea. Al
#  final deberías de tener 7 tablas en =star_wars.db=

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


# Ejercicio C:
#- Repite el inciso anterior, pero ahora usando =aws= y =parallel=. Crea 7 instancias de =Amazon EC2=,
# en cada una procesa como antes. Distribuye los archivos de ejecución y luego tráelos a tu máquina local para 
#guardarlos en una base de datos =sqlite=.