library(shiny)
library(DT)
library(RNeo4j)
library(dplyr)
library(ggplot2)

shinyUI(fluidPage(
  
  titlePanel('Análisis de Corrupción en las Compras del Gobierno'),
    
    tabsetPanel(
          
      tabPanel('Dependencias', 
               column(7, DT::dataTableOutput('tabla_dependencia')),
               column(5, plotOutput('grafica_dependencia', height = 500))),
          
      tabPanel('Unidades Compradoras', 
               column(7, DT::dataTableOutput('tabla_unidades')),
               column(5, plotOutput('grafica_unidades', height = 500))),
          
      tabPanel('Compras', 
               column(6, DT::dataTableOutput('tabla_compras')),
               column(6, plotOutput('grafica_compras', height = 500))),
      
      tabPanel('Funcionarios', 
               column(7, tableOutput('rel_funcionario_proveedor')),
               column(7, plotOutput('grafica_funcionario_2')),
               column(7, plotOutput('grafica_funcionario_1'))),
      
      tabPanel('Proveedores', 
               column(7, DT::dataTableOutput('tabla_proveedores')),
               column(5, plotOutput('grafica_proveedores', height = 500)))
               #column(7, visNetworkOutput('rel_proveedor_funcionario')))
      

  )
))
