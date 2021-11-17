#app.R

library(googlesheets4)
library(reticulate)

table <- "responses"

saveData <- function(data) {
  library(tidyverse)
  # The data must be a dataframe rather than a named vector
  data <- data %>% as.list() %>% data.frame()
  # Add the data as a new row
  sheet_append(sheet_url, data)
}

loadData <- function(sheet_url) {
  # Read the data
  read_sheet(sheet_url)
}



d <- read_csv('https://raw.githubusercontent.com/seescoto/cds302_model_app/main/credit_risk_dataset.csv')

d


source_python('python_model.py')

