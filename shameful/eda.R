rm(list=ls())
source("./utils.R")

# Eda shameful ya tiene conexión a la base de datos. 
# con -> conección directa
# con_raw -> conección al schema raw
# e.g. requests <- tbl(con, sql("SELECT * from schema.table WHERE condition"))


# EDA Funcionarios
funcionarios <- tbl(con_raw, "funcionarios")
head(funcionarios)
dplyr::count(funcionarios,institucion) %>% View()


# EDA Compranet
compranet <- tbl(con_raw, "compranet")
head(compranet)
compranet %>% dplyr::select()
count(compranet,DEPENDENCIA, CLAVEUC) %>% View()
