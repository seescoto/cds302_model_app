library(shiny)


#user interface so they can interact with stuff
ui <- fluidPage(
  
  # App title ----
  titlePanel(" Will you get approved for a loan?"),
  
  #  sidebarlayout takes sidebar panel, main panel, position, fluid
    sidebarLayout(
      sidebarPanel(
                 sliderInput(inputId = 'percent_int', #what we enter into predict()
                             label = "What is the highest percent interest you're willing to pay?",
                             min = 0, max = 36, value = 10 #avg interest rate
                    ),
      
         
                #income  input
                textInput(inputId = 'income',
                          label = "What is your yearly income?",
                          value = '50000'),
      
                
                #loan amount input
                textInput(inputId = 'loan',
                          label = "How much money would you like to borrow?",
                          value = '10000')),
        

  
  # Main panel for displaying outputs ----
      mainPanel(
        # Output: Formatted text for caption ----
        #h3(textOutput("caption")),
        
        # Output: Plot of the requested variable against mpg ----
        #plotOutput("mpgPlot")
        
      ),
  position = 'right',
  fluid = TRUE
  
  
  )) 



#predict function based on our lrm (glm family = binomial)
server <- function(input, output, session) {
  
  dfinput <- reactive({
    switch(input$dataset,
           "percent_int" = percent_int,
           "loan_percent" = loan/income)
  
  })
}


shinyApp(ui, server)
