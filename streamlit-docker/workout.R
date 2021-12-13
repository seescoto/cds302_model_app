#app.R

library(googlesheets4)
library(reticulate)
library(tidyverse)
library(modelr)

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


mod <- glm(loan_status ~ loan_percent_income + interest_rate, data = X_train, 
           family = 'binomial')

summary(mod)

d %>% 
  ggplot() +
  geom_jitter(aes(loan_percent_income, loan_int_rate, color = loan_status))

mod2 <- glm(loan_status ~ loan_percent_income * loan_int_rate, data = d, 
            family = 'binomial')

summary(mod2)


new <- tibble(loan_percent_income = .59, 
                 loan_int_rate = 11.02) 

add_predictions(mod2, type = 'response', data = new)

mod2 %>% 
  add1(scope = colnames(d)) %>% 
  arrange(AIC)

#merging training datasets together to get loan status in there
xy_train <- merge(X_train, y_train )
xy_train <- X_train
xy_train$loan_status <- y_train


#trying first log reg model

mod <- glm(loan_status ~ loan_percent_income + interest_rate, data = xy_train, 
           family = 'binomial')
summary(mod)

#scond log reg model
mod2 <- glm(loan_status ~ loan_percent_income * interest_rate, data = xy_train, 
            family = 'binomial')
summary(mod2)

#comparing
AIC(mod, mod2)
#mod2 has a significantly lower aic even though df is higher, meaning it's better
#but precision/accuracy, specificity are slightly lower so nah


#calculating recall, precision, etc
xy_test <- X_test
xy_test$loan_status <- y_test

#adding predicted loan status
xy_test <- add_predictions(data = xy_test, mod, var = 'pred_loan_status', type = 'response') 

#making columns of true negatives, false negatives, etc.
xy_test <- xy_test %>% 
  mutate(status = case_when(loan_status == 0 & pred_loan_status < 0.5 ~ 'TN',
                           loan_status == 0 & pred_loan_status >= 0.5 ~ 'FP',
                           loan_status == 1 & pred_loan_status >= 0.5 ~ 'TP',
                           TRUE ~ 'FP' #all other cases are false positive
                           ))

num_fp <- which(xy_test$status == 'FP') %>% 
  length()

num_tp <- which(xy_test$status == 'TP') %>% 
  length()
num_fn <- which(xy_test$status == 'FN') %>% 
  length()
num_tn <- which(xy_test$status == 'TN') %>% 
  length()

accuracy <- (num_tp + num_tn)/(length(xy_test$status))
specificity <- num_tn/(num_tn + num_fp)
precision <- num_tp/ (num_tp + num_fp)
recall <- num_tp/(num_tp + num_fn)

print(paste(accuracy, specificity, precision, recall))


which(xy_test$status == 'FN')

xy_test %>% 
  filter(status == 'TN') %>%  count()
num_tn

xy_test %>% 
  filter(pred_loan_status < 0.5, loan_status == 1)

xy_test
