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




library(tidyverse)
library(modelr)
d <- read_csv('https://raw.githubusercontent.com/seescoto/cds302_model_app/main/credit_risk_dataset.csv')

mod <- glm(loan_status ~ loan_percent_income + loan_int_rate, data = d, 
           family = 'binomial')

summary(mod)

d %>% 
  ggplot() +
  geom_point(aes(loan_percent_income, loan_int_rate, color = loan_status))

mod2 <- glm(loan_status ~ loan_percent_income * loan_int_rate, data = d, 
            family = 'binomial')

summary(mod2)



new <- data_frame(loan_percent_income = .59, 
                 loan_int_rate = 11.02) 

add_predictions(mod, type = 'response', data = new)
