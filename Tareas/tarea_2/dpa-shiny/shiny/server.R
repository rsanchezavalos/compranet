library(shiny)
library(curl)

# Define server logic required to draw a histogram
shinyServer(function(input, output) {

  tmp <- tempfile()
  curl_download("http://0.0.0.0:8080/", tmp)
  readLines(tmp)

    output$text1 <- renderText({ 
    readLines(tmp)
  })
  
})


