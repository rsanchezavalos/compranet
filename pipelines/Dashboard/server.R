library(shiny)
library(DT)
library(RNeo4j)
library(dplyr)

source('./utils.R')

# agregar también por año

# Define server logic required to draw a histogram
shinyServer(function(input, output) {
  
  compranet <- reactive({
    # Abrir base de datos compranet
    compranet <- db_schema_con("raw")
  })
  
  neo <- reactive({
    # Conectar con neo4j
    graph = startGraph("http://ec2-54-69-4-123.us-west-2.compute.amazonaws.com:7474/db/data/")
    dependencia = getLabeledNodes(graph, "Dependencia")
  })
  
#  indices <- reactive({
    # Abrir resultados de los indices
#  })

  # Tabla resumen por dependencia
    
  output$tabla_dependencia <- DT::renderDataTable({
    
    datos <- compranet()
    datos <- datos[which(datos$MONEDA == 'MXN'), ]
    
    operaciones <- aggregate(IMPORTE_CONTRATO ~ DEPENDENCIA, FUN = NROW, data = datos)
    monto_maximo <- aggregate(IMPORTE_CONTRATO ~ DEPENDENCIA, FUN = max, data = datos)
    monto_minimo <- aggregate(IMPORTE_CONTRATO ~ DEPENDENCIA, FUN = min, data = datos)
    monto_promedio <- aggregate(IMPORTE_CONTRATO ~ DEPENDENCIA, FUN = mean, data = datos)
    monto_total <- aggregate(IMPORTE_CONTRATO ~ DEPENDENCIA, FUN = sum, data = datos)
    
    tabla <- merge(operaciones, monto_maximo, by = 'DEPENDENCIA')
    tabla <- merge(tabla, monto_minimo, by = 'DEPENDENCIA')
    tabla <- merge(tabla, monto_promedio, by = 'DEPENDENCIA')
    tabla <- merge(tabla, monto_total, by = 'DEPENDENCIA')
    colnames(tabla) <- c('DEPENDENCIA', 'NÚMERO DE TRANSACCIONES', 'MÁXIMO', 'MÍNIMO', 'PROMEDIO', 'TOTAL')
    
    tabla 
    
  })
  
  # Tabla resumen por unidad compradora
  
  output$tabla_unidades <- DT::renderDataTable({
    
    datos <- compranet()
    datos <- datos[which(datos$MONEDA == 'MXN'), ]
    
    operaciones <- aggregate(IMPORTE_CONTRATO ~ NOMBRE_DE_LA_UC, FUN = NROW, data = datos)
    monto_maximo <- aggregate(IMPORTE_CONTRATO ~ NOMBRE_DE_LA_UC, FUN = max, data = datos)
    monto_minimo <- aggregate(IMPORTE_CONTRATO ~ NOMBRE_DE_LA_UC, FUN = min, data = datos)
    monto_promedio <- aggregate(IMPORTE_CONTRATO ~ NOMBRE_DE_LA_UC, FUN = mean, data = datos)
    monto_total <- aggregate(IMPORTE_CONTRATO ~ NOMBRE_DE_LA_UC, FUN = sum, data = datos)
    
    tabla <- merge(operaciones, monto_maximo, by = 'NOMBRE_DE_LA_UC')
    tabla <- merge(tabla, monto_minimo, by = 'NOMBRE_DE_LA_UC')
    tabla <- merge(tabla, monto_promedio, by = 'NOMBRE_DE_LA_UC')
    tabla <- merge(tabla, monto_total, by = 'NOMBRE_DE_LA_UC')
    colnames(tabla) <- c('UNIDAD COMPRADORA', 'NÚMERO DE TRANSACCIONES', 'MÁXIMO', 'MÍNIMO', 'PROMEDIO', 'TOTAL')
    
    tabla 
    
  })

  # Tabla resumen por título del expediente
  
  output$tabla_compras <- DT::renderDataTable({
    
    datos <- compranet()
    datos <- datos[which(datos$MONEDA == 'MXN'), ]
    
    operaciones <- aggregate(IMPORTE_CONTRATO ~ TITULO_EXPEDIENTE, FUN = NROW, data = datos)
    monto_total <- aggregate(IMPORTE_CONTRATO ~ TITULO_EXPEDIENTE, FUN = sum, data = datos)
    
    tabla <- merge(operaciones, monto_total, by = 'TITULO_EXPEDIENTE')
    colnames(tabla) <- c('DESCRIPCIÓN DE LA COMPRA', 'NÚMERO DE EXPEDIENTES', 'MONTO TOTAL')
    
    tabla 
    
  })  
  
  # Tabla resumen por proveedor
  
  output$tabla_proveedores <- DT::renderDataTable({
    
    datos <- compranet()
    datos <- datos[which(datos$MONEDA == 'MXN'), ]
    
    operaciones <- aggregate(IMPORTE_CONTRATO ~ PROVEEDOR_CONTRATISTA, FUN = NROW, data = datos)
    monto_maximo <- aggregate(IMPORTE_CONTRATO ~ PROVEEDOR_CONTRATISTA, FUN = max, data = datos)
    monto_minimo <- aggregate(IMPORTE_CONTRATO ~ PROVEEDOR_CONTRATISTA, FUN = min, data = datos)
    monto_promedio <- aggregate(IMPORTE_CONTRATO ~ PROVEEDOR_CONTRATISTA, FUN = mean, data = datos)
    monto_total <- aggregate(IMPORTE_CONTRATO ~ PROVEEDOR_CONTRATISTA, FUN = sum, data = datos)
    
    tabla <- merge(operaciones, monto_maximo, by = 'PROVEEDOR_CONTRATISTA')
    tabla <- merge(tabla, monto_minimo, by = 'PROVEEDOR_CONTRATISTA')
    tabla <- merge(tabla, monto_promedio, by = 'PROVEEDOR_CONTRATISTA')
    tabla <- merge(tabla, monto_total, by = 'PROVEEDOR_CONTRATISTA')
    colnames(tabla) <- c('PROVEEDOR', 'NÚMERO DE TRANSACCIONES', 'MÁXIMO', 'MÍNIMO', 'PROMEDIO', 'TOTAL')
    
    tabla 
    
  })
  
  #  Histogrma gastos por dependencia
  
  output$grafica_dependencia <- renderPlot({
    
    datos <- compranet()
    datos <- datos[which(datos$MONEDA == 'MXN'), ]
    
    sel <- input$tabla_dependencia_rows_selected
    
    operaciones <- aggregate(IMPORTE_CONTRATO ~ DEPENDENCIA, FUN = NROW, data = datos)
    monto_maximo <- aggregate(IMPORTE_CONTRATO ~ DEPENDENCIA, FUN = max, data = datos)
    monto_minimo <- aggregate(IMPORTE_CONTRATO ~ DEPENDENCIA, FUN = min, data = datos)
    monto_promedio <- aggregate(IMPORTE_CONTRATO ~ DEPENDENCIA, FUN = mean, data = datos)
    monto_total <- aggregate(IMPORTE_CONTRATO ~ DEPENDENCIA, FUN = sum, data = datos)
    
    tabla <- merge(operaciones, monto_maximo, by = 'DEPENDENCIA')
    tabla <- merge(tabla, monto_minimo, by = 'DEPENDENCIA')
    tabla <- merge(tabla, monto_promedio, by = 'DEPENDENCIA')
    tabla <- merge(tabla, monto_total, by = 'DEPENDENCIA')
    colnames(tabla) <- c('DEPENDENCIA', 'NÚMERO DE TRANSACCIONES', 'MÁXIMO', 'MÍNIMO', 'PROMEDIO', 'TOTAL')
    
    tabla2 <- tabla[sel, ]
    
    datos2 <- datos[which(datos$DEPENDENCIA %in% tabla2[ , 1]), ]
    
    hist(datos$IMPORTE_CONTRATO, breaks = 200)
    
    ifelse(length(sel > 0),
           grafica <- hist(datos2$IMPORTE_CONTRATO, breaks = 200),
           grafica <- hist(datos$IMPORTE_CONTRATO, breaks = 200))
    
    grafica
    
  })

  # Histograma gastos por unidad compradora
  
  output$grafica_unidades <- renderPlot({
    
    datos <- compranet()
    datos <- datos[which(datos$MONEDA == 'MXN'), ]
    
    sel <- input$tabla_unidades_rows_selected
    
    operaciones <- aggregate(IMPORTE_CONTRATO ~ NOMBRE_DE_LA_UC, FUN = NROW, data = datos)
    monto_maximo <- aggregate(IMPORTE_CONTRATO ~ NOMBRE_DE_LA_UC, FUN = max, data = datos)
    monto_minimo <- aggregate(IMPORTE_CONTRATO ~ NOMBRE_DE_LA_UC, FUN = min, data = datos)
    monto_promedio <- aggregate(IMPORTE_CONTRATO ~ NOMBRE_DE_LA_UC, FUN = mean, data = datos)
    monto_total <- aggregate(IMPORTE_CONTRATO ~ NOMBRE_DE_LA_UC, FUN = sum, data = datos)
    
    tabla <- merge(operaciones, monto_maximo, by = 'NOMBRE_DE_LA_UC')
    tabla <- merge(tabla, monto_minimo, by = 'NOMBRE_DE_LA_UC')
    tabla <- merge(tabla, monto_promedio, by = 'NOMBRE_DE_LA_UC')
    tabla <- merge(tabla, monto_total, by = 'NOMBRE_DE_LA_UC')
    colnames(tabla) <- c('UNIDAD COMPRADORA', 'NÚMERO DE TRANSACCIONES', 'MÁXIMO', 'MÍNIMO', 'PROMEDIO', 'TOTAL')
    
    tabla2 <- tabla[sel, ]
    
    datos2 <- datos[which(datos$NOMBRE_DE_LA_UC %in% tabla2[ , 1]), ]
    
    hist(datos$IMPORTE_CONTRATO, breaks = 200)
    
    ifelse(length(sel > 0),
           grafica <- hist(datos2$IMPORTE_CONTRATO, breaks = 200),
           grafica <- hist(datos$IMPORTE_CONTRATO, breaks = 200))
    
    grafica
    
  })
  
    # Histograma gastos por proveedor
  
  output$grafica_compras <- renderPlot({
    
    datos <- compranet()
    datos <- datos[which(datos$MONEDA == 'MXN'), ]
    
    sel <- input$tabla_compras_rows_selected
    
    operaciones <- aggregate(IMPORTE_CONTRATO ~ TITULO_EXPEDIENTE, FUN = NROW, data = datos)
    monto_total <- aggregate(IMPORTE_CONTRATO ~ TITULO_EXPEDIENTE, FUN = sum, data = datos)
    
    tabla <- merge(operaciones, monto_total, by = 'TITULO_EXPEDIENTE')
    colnames(tabla) <- c('DESCRIPCIÓN DE LA COMPRA', 'NÚMERO DE EXPEDIENTES', 'MONTO TOTAL')
    
    tabla2 <- tabla[sel, ]
    
    datos2 <- datos[which(datos$TITULO_EXPEDIENTE %in% tabla2[ , 1]), ]
    
    hist(datos$IMPORTE_CONTRATO, breaks = 200)
    
    ifelse(length(sel > 0),
           grafica <- hist(datos2$IMPORTE_CONTRATO, breaks = 200),
           grafica <- hist(datos$IMPORTE_CONTRATO, breaks = 200))
    
    grafica
    
    })
  
  # Histograma gastos por proveedor
  
  output$grafica_proveedores <- renderPlot({
    
    datos <- compranet()
    datos <- datos[which(datos$MONEDA == 'MXN'), ]
    
    sel <- input$tabla_proveedores_rows_selected
    
    operaciones <- aggregate(IMPORTE_CONTRATO ~ PROVEEDOR_CONTRATISTA, FUN = NROW, data = datos)
    monto_maximo <- aggregate(IMPORTE_CONTRATO ~ PROVEEDOR_CONTRATISTA, FUN = max, data = datos)
    monto_minimo <- aggregate(IMPORTE_CONTRATO ~ PROVEEDOR_CONTRATISTA, FUN = min, data = datos)
    monto_promedio <- aggregate(IMPORTE_CONTRATO ~ PROVEEDOR_CONTRATISTA, FUN = mean, data = datos)
    monto_total <- aggregate(IMPORTE_CONTRATO ~ PROVEEDOR_CONTRATISTA, FUN = sum, data = datos)
    
    tabla <- merge(operaciones, monto_maximo, by = 'PROVEEDOR_CONTRATISTA')
    tabla <- merge(tabla, monto_minimo, by = 'PROVEEDOR_CONTRATISTA')
    tabla <- merge(tabla, monto_promedio, by = 'PROVEEDOR_CONTRATISTA')
    tabla <- merge(tabla, monto_total, by = 'PROVEEDOR_CONTRATISTA')
    colnames(tabla) <- c('PROVEEDOR', 'NÚMERO DE TRANSACCIONES', 'MÁXIMO', 'MÍNIMO', 'PROMEDIO', 'TOTAL')
    
    tabla2 <- tabla[sel, ]
    
    datos2 <- datos[which(datos$PROVEEDOR_CONTRATISTA %in% tabla2[ , 1]), ]
    
    hist(datos$IMPORTE_CONTRATO, breaks = 200)
    
    ifelse(length(sel > 0),
           grafica <- hist(datos2$IMPORTE_CONTRATO, breaks = 200),
           grafica <- hist(datos$IMPORTE_CONTRATO, breaks = 200))
    
    grafica
    
  })
  
    
})
