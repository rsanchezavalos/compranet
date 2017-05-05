rm(list=ls())
source("./utils.R")

# Eda Shameful ya tiene conexión a la base de datos. 
# con -> conección directa
# e.g. requests <- tbl(con, sql("SELECT * from schema.table WHERE condition"))
# Bib -> https://cran.r-project.org/web/packages/dplyr/vignettes/databases.html

con_raw <- db_schema_con("raw")

data <- fill_NAs(data)

data <- fix_Ramo(con_raw)

data <- fix_Folio(data)


con = src_postgres(user=conf$PGUSER, 
                   password=conf$PGPASSWORD, 
                   host=conf$PGHOST, port=5432, 
                   dbname=dbname,
                   options=paste0("-c search_path=",schema))

dbWriteTable(con, c("clean",'compranet'), data, row.names=FALSE)
