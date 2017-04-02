###############
# Compranet
###############

echo "Descarga Compranet De 2002 a 2011"
# Descargar
wget --no-check-certificate http://compranetinfo.funcionpublica.gob.mx/descargas/cnet3/EX{2002..2011}.xlsx -P ./temp
wget --no-check-certificate http://compranetinfo.funcionpublica.gob.mx/descargas/cnet3/LP{2002..2011}.xlsx -P ./temp

for filename in $(ls ./temp/*.xlsx)
	in2csv $filename | sed '1d' | sed -e ':a;s/^\(\("[^"]*"\|'\''[^'\'']*'\''\|[^",'\'']*\)*\),/\1\|/;ta' >> ./temp/2002_2011.csv

echo "Descarga Compranet De 2010 a 2017"

wget --no-check-certificate  https://compranetinfo.funcionpublica.gob.mx/descargas/cnet/Contratos2010_2012.zip 
wget --no-check-certificate  https://upcp.funcionpublica.gob.mx/descargas/Contratos{2013..2017}.zip 
for f (./*.zip) unzip $f 

rm *.zip
find . -name '*.xlsx' | parallel ssconvert -T Gnumeric_stf:stf_csv {} \;
rm *.xlsx

# ToDo()
# Hace falta revisar la versión del documento antes del cambio que es del tipo 170302082128
# tenemos que guardar esta información - puede ser algo como esto:
for f (./*.csv) echo "${f%_*.*} version $f" >> metadata.txt

cat $( ls *.csv ) | sed '1d' | sed -e ':a;s/^\(\("[^"]*"\|'\''[^'\'']*'\''\|[^",'\'']*\)*\),/\1\t/;ta' >> 2012_2017.csv