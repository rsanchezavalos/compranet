rm(list=ls())
source("./utils.R")

# Ingest Compranet - Temporal

data <- read_csv("../data/compranet/base_final.csv")
data["X1"]<-NULL
dbWriteTable(con, c("raw",'compranet'),data, row.names=FALSE)

