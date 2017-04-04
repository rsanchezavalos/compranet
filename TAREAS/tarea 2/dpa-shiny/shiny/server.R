#
# This is the server logic of a Shiny web application. You can run the 
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)
library(httr)

# Define server logic required to draw a histogram
shinyServer(function(input, output) {
  r <- GET("http://localhost:8080/")  
  output$text1 <- renderText({ 
    content(r, "text")
  })
  
})


