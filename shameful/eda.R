rm(list=ls())
source("./utils.R")

# Eda Shameful ya tiene conexión a la base de datos. 
# con -> conección directa
# e.g. requests <- tbl(con, sql("SELECT * from schema.table WHERE condition"))
# Bib -> https://cran.r-project.org/web/packages/dplyr/vignettes/databases.html

con_raw <- db_schema_con("raw")

# EDA Funcionarios
funcionarios <- tbl(con_raw, "funcionarios")
head(funcionarios)
dplyr::count(funcionarios,nombre, primer_apellido,segundo_apellido) %>% filter(n<2) %>% 
  arrange(desc(n)) %>% group_by(n) %>% summarize(conteo = n()) %>% arrange(desc(conteo)) %>% write.csv("temp.csv",row.names = FALSE)


# EDA Compranet
compranet <- tbl(con_raw, "compranet")
head(compranet)
compranet %>% dplyr::select()
count(compranet,DEPENDENCIA, CLAVEUC) %>% View()
