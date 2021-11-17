library(shiny)


#user interface so they can interact with stuff
ui <- pageWithSidebar(
  
  # App title ----
  titlePanel(" Will you get approved for a loan?"),
  
  
  
  #  inputs ---- should be loan percent rate and loan_percent_income
    sidebarLayout(
      sidebarPanel(
        sliderInput(inputId = 'percent_int', #what we enter into predict()
                    label = "What is the highest percent interest you're willing to pay?",
                    min = 0,
                    max = 36, #max
                    value = 10 #avg interest rate
                    ),
        
        #income  input
        textInput(inputId = 'income',
                  label = "What is your yearly income?",
                  value = '50000'),
        
        #loan amount input
        textInput(inputId = 'loan',
                  label = "How much money would you like to borrow?",
                  value = '10000')
        
                   ),
      
                  
      
 
  
  
  # Main panel for displaying outputs ----
      mainPanel()
                )
)

#predict function based on our lrm
server <- function(input, output, session) {
  
}


shinyApp(ui, server)
