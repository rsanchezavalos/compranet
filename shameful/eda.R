rm(list=ls())
source("./utils.R")

# Connect to Raw DB
my_db <- src_sqlite("../Ingest/raw.db", create = T)

# EDA Funcionarios
funcionarios <- tbl(my_db,"funcionarios")
dplyr::count(funcionarios,institucion) %>% View()
