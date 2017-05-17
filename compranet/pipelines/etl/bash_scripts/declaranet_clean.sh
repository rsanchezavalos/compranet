#! /bin/bash
# Función para crear archivo de texto

declaranet_to_txt () {
	pdftotext -layout "$1" 
}

function txt_to_csv () {	
	NOMBRE=$(cat $1 | grep "NOMBRE(S).*" | sed "s/NOMBRE(S)\: *//g;s/^ //g");
	echo $NOMBRE;

	f=$(cat $1 |  sed -ne '/EXPERIENCIA LABORAL/,$p;' | sed -e 's/EXPERIENCIA LABORAL.*//g' | \
	sed -e '/SI ESTOY DE ACUERDO\|EL SERVIDOR NO A\|EL SERVIDOR PÚBLICO/,$d');


	#base="${f%.[^.]*}"
	AMBITO=$( echo "$f" | grep -o ".*AMBITO" |  sed "s/ AMBITO\.*//g" | wc --chars );
	PODER=$( echo "$f" | grep -o ".*PODER" |  sed "s/  PODER\.*//g" | wc --chars );
	INSTITUCION=$( echo "$f" | grep -o ".*INSTITUCIÓN O " |  sed  "s/ INSTITUCI.*N O\.*//g" | wc --chars );
	PUESTO=$( echo "$f" | grep -o ".*  PUESTO" |  sed "s/ PUESTO\.*//g" | wc --chars );
	FUNCION=$( echo "$f" | grep -o ".*FUNCIÓN PRINCIPAL" |  sed "s/CIÓN PRINCIPAL\.*//g" | wc --chars );
	INGRESO=$( echo "$f" | grep -o ".*INGRESO - EGRESO" | sed "s/SO \- EGRESO\.*//g" |  wc --chars );
	UNIDAD=$( echo "$f" | grep -o -m 1 ".*ADMINISTRATIVA" |  sed  "s/ADMINISTRATIVA\.*//" | wc --chars );

	echo "$f" | sed "s/^\(.\{"$PODER"\}\)/\1|/;s/^\(.\{"$AMBITO"\}\)/\1|/;s/^\(.\{"$INSTITUCION"\}\)/\1|/;s/^\(.\{"$UNIDAD"\}\)/\1|/;s/^\(.\{"$PUESTO"\}\)/\1|/;s/^\(.\{"$FUNCION"\}\)/\1|/;s/^\(.\{"$INGRESO"\}\)/\1|/;s/^/$NOMBRE|/g;" | awk '!/INGRESO - EGRESO|INSTITUCIÓN O|EMPRESA   /' |  awk 'BEGIN {FS = OFS = "|"} {$9 = $9; print}' | sed '1s/.*/NOMBRE|SECTOR|PODER|AMBITO|INSTITUCION_O_EMPRESA|UNIDAD_ADMINISTRATIVA|PUESTO|FUNCION_PRINCIPAL|INGRESO_EGRESO/g'
}

