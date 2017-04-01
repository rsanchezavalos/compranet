##################
## Packages
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

fill_NAs <- function(data_frame) {
  for (i in 1:nrow(data_frame)) {
    for (j in 1:ncol(data_frame)) {
      ifelse(data_frame[i,j] == '',
             data_frame[i,j] <- NA,
             data_frame[i,j] <- data_frame[i,j])
    }
  }
  
}

cormat_NAs <- function(data_frame) {
  
  porccol <- apply(is.na(data_frame), 1, sum)/ncol(data_frame)
  porcrow <- apply(is.na(data_frame), 2, sum)/nrow(data_frame)
  compporc <- sum(complete.cases(data_frame))/nrow(data_frame)
  
  if(compporc!=1){
    colsmasfalta <- paste(sort(porcrow[porcrow>0], decreasing = TRUE) %>%
                            names(), collapse = ", ")
    
    cor.mat <- cor(is.na(data_frame)[,porcrow>0] )
    tab.corr <- cor.mat %>%
      tbl_df() %>%
      mutate(rows = colnames(cor.mat)) %>%
      gather(cols, corr, -rows)
    gg <- ggplot(tab.corr, aes(x = rows, y = cols, fill = corr)) +
      geom_tile(alpha =.7) +
      geom_text(aes(label = round(corr, 2), color = corr)) +
      scale_fill_continuous(low = 'white', high = "#132B43") +
      scale_color_continuous(high = 'white', low = "#132B43") +
      xlab(NULL) +
      ylab(NULL) +
      ggtitle('cormat_Nas') +
      theme(legend.position = 'none',
            plot.title = element_text(hjust=0, size=9),
            axis.text.x = element_text(angle = 90, hjust = 1)) +
      coord_fixed(ratio = .65)
    return(gg)
  }
  else{
    warning("No missing values")
  }
}
