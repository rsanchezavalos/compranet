#! /bin/bash
# Función para crear archivo de texto
export LANG=C.UTF-8

#RAW PDF LOCATION
#../../../../data/declaranet/cv/

#OUTPUT FILE NAME
OUTPUT="../../data/declaranet/cv_to_text.txt"

if [ ! -e "$OUTPUT" ] ; then
	echo 'NOMBRE|SECTOR|PODER|AMBITO|INSTITUCION_O_EMPRESA|UNIDAD_ADMINISTRATIVA|PUESTO|FUNCION_PRINCIPAL|INGRESO_EGRESO' > $OUTPUT
fi

for filename in $1;
do	  
	#echo $filename
	f=$( pdftotext -layout $filename - )
	#echo $f
	FUNCIONARIO=$( echo "$f" | grep "NOMBRE(S).*" | sed "s/NOMBRE(S)\: *//g;s/^ //g")
	FILE="$( echo "$f" |  sed -ne '/EXPERIENCIA LABORAL/,$p;' | sed -e 's/EXPERIENCIA LABORAL.*//g' | \
	 sed -e '/SI ESTOY DE ACUERDO\|EL SERVIDOR NO A\|EL SERVIDOR PÚBLICO/,$d' )"

	base="${f%.[^.]*}"
	AMBITO=$( echo "$FILE" | grep -o ".*AMBITO" |  sed "s/ AMBITO\.*//g" | wc --chars )
	PODER=$( echo "$FILE" | grep -o ".*PODER" |  sed "s/  PODER\.*//g" | wc --chars )
	INSTITUCION=$( echo "$FILE" | grep -o ".*INSTITUCIÓN O " |  sed  "s/ INSTITUCI.*N O\.*//g" | wc --chars )
	PUESTO=$( echo "$FILE" | grep -o ".*  PUESTO" |  sed "s/ PUESTO\.*//g" | wc --chars )
	FUNCION=$( echo "$FILE" | grep -o ".*FUNCIÓN PRINCIPAL" |  sed "s/CIÓN PRINCIPAL\.*//g" | wc --chars )
	INGRESO=$( echo "$FILE" | grep -o ".*INGRESO - EGRESO" | sed "s/SO \- EGRESO\.*//g" |  wc --chars )
	UNIDAD=$( echo "$FILE" | grep -o -m 1 ".*ADMINISTRATIVA" |  sed  "s/ADMINISTRATIVA\.*//" | wc --chars )
	echo "$FILE" | sed "s/^/\|/g;s/^\(.\{"$PODER"\}\)/\1|/;s/^\(.\{"$AMBITO"\}\)/\1|/;s/^\(.\{"$INSTITUCION"\}\)/\1|/;s/^\(.\{"$UNIDAD"\}\)/\1|/;s/^\(.\{"$PUESTO"\}\)/\1|/;s/^\(.\{"$FUNCION"\}\)/\1|/;s/^\(.\{"$INGRESO"\}\)/\1|/;s/^/$FUNCIONARIO/;" | \
	awk '!/INGRESO - EGRESO|INSTITUCIÓN O|EMPRESA   /' |  awk 'BEGIN {FS = OFS = "|"} {$9 = $9; print}' >> $OUTPUT

done;