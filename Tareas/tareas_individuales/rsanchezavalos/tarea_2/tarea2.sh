# Código para leer la base de datos

head -n -2 "$resource".json >> "$resource"_clean.json
echo -e }"\n"]>>"$resource"_clean.json
in2csv -f json -v "$resource"_clean.json > "$resource".csv
csvsql --db sqlite:///star_wars.db --insert "$resource".csv
done
