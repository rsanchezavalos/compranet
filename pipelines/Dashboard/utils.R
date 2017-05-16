##################
### Packages
##################
print("Descargando paquetes")
.packages = c('lubridate', 'magrittr', 'ggvis', 'dplyr', 'tidyr', 'readr', 'rvest',
              'ggplot2', 'stringr', 'ggthemes', 'googleVis', 'shiny', 'tibble', 'vcd', 'vcdExtra',
              'GGally','curl','gdata','readxl','ggmap','jsonlite','RPostgreSQL')


# Install CRAN packages (if not already installed)
.inst <- .packages %in% installed.packages()
if(length(.packages[!.inst]) > 0) install.packages(.packages[!.inst])

# Load packages into session 
lapply(.packages, require, character.only=TRUE)


##################
## Create Connection to DB
##################
print("Conectandose a CompranetDB")
conf <- fromJSON("../config/conf_profile.json")
#pg = dbDriver("PostgreSQL")
#con = dbConnect(pg, user=conf$PGUSER, password=conf$PGPASSWORD,
#                host=conf$PGHOST, port=5432, dbname=conf$PGDATABASE)

##################
## Functions
##################
#Dplyr connection
db_schema_con <- function(schema,dbname=conf$PGDATABASE){
  con = src_postgres(user=conf$PGUSER, 
                     password=conf$PGPASSWORD, 
                     host=conf$PGHOST, port=5432, 
                     dbname=dbname,
                     options=paste0("-c search_path=",schema))
  return(con)
}

