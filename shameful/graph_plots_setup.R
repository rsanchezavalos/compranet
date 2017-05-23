instalar <- function(paquete) {
  if (!require(paquete,character.only = TRUE, 
               quietly = TRUE, 
               warn.conflicts = FALSE)) {
    install.packages(as.character(paquete), 
                     dependencies = TRUE, 
                     repos = "http://cran.us.r-project.org")
    library(paquete, 
            character.only = TRUE, 
            quietly = TRUE, 
            warn.conflicts = FALSE)
  }
}

paquetes <- c('dplyr', 'lubridate', 'ggplot2', 'tidyr', 'Hmisc', 'RColorBrewer', 'psych', 'knitr', 'vcd',
              'devtools', 'readxl', 'stringr', 'foreign', 'lattice', 'GGally', 'RNeo4j', 'network', 'sna',
              'igraph', 'visNetwork')

lapply(paquetes, instalar)
rm(paquetes, instalar)