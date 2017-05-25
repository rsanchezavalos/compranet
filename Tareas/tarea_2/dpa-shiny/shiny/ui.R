library(shiny)

# Define UI for application that draws a histogram
shinyUI(fluidPage(
  
  # Application title
  titlePanel("Descargando data"),
  mainPanel(
    textOutput("text1")
  )
  )
)
