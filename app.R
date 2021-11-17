library(shiny)


ui <- pageWithSidebar(
  
  # App title ----
  headerPanel("Will you get approved for a loan?"),
  
  # Sidebar panel for inputs ----
  sidebarPanel(),
  
  # Main panel for displaying outputs ----
  mainPanel()
)