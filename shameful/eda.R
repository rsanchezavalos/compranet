rm(list=ls())
source("./utils.R")

# Connect to Raw DB
my_db <- src_sqlite("./raw.db", create = T)

# EDA Funcionarios
funcionarios <- tbl(my_db,"funcionarios")
dplyr::count(funcionarios,institucion) %>% View()

# EDA Compranet 2002 a 2011
# compranet_2002_2011 <- tbl(my_db, "compranet_2002_2011")
compranet_2002_2012 <- read.csv('./2002_2011.csv')

# EDA Compranet 2012 a 2017
# compranet_2012_2017 <- tbl(my_db, "compranet_2012_2017")
compranet_2012_2017 <- read.csv('./2012_2017.csv')
