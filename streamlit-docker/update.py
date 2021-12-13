###updated csv file so no need to redo each time


import pandas as pd

path = 'https://raw.githubusercontent.com/seescoto/cds303_model_app/main/credit_risk_dataset.csv'
df = pd.read_csv(path)
#drop categorical data
credit_risk = df.select_dtypes(exclude=['object'])
#renaming columns
#Renaming columns
credit_risk.columns = ['age', 'income', 'employment_length', 'amount', 'interest_rate',
 'loan_status', 'loan_percent_income', 'credit_length']
#mean imputation
credit_risk["interest_rate"].fillna(credit_risk["interest_rate"].mean(), inplace = True)
#getting important cols for model (based on what correlates with loan status)
Feature_cols = ['interest_rate', 'loan_percent_income']

credit_risk.to_csv('updated_csv.csv')
