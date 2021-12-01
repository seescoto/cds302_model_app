###streamlit app - sofia escoto

import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
import numpy as np


#title and stuff idk
st.title('Credit Loan Risk')
st.subheader('Will you get approved for a loan?')




# data and model loading
data_load_state = st.text('Loading data and model...')

#loading data
path = 'https://raw.githubusercontent.com/seescoto/cds302_model_app/main/credit_risk_dataset.csv'
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

#fitting the model
#setting x and y
X = credit_risk[Feature_cols]
y = credit_risk.loan_status
#split into test/train sets - no randomness so same results each time
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.20, random_state = 0)
#creating model and fitting it
logreg = LogisticRegression()
logreg.fit(X_train, y_train)

#model and data fitted!
data_load_state.text('Loading data and model... done!')





###inputs
#loan amount
loan_amt = st.number_input('How much money would you like to loan in dollars?', value = 10000)
if loan_amt <= 0:
    st.error('Loan amount must be a positive non-zero value.')
#income
income = st.number_input('What is your annual income in dollars?', value = 50000)
if income < 0:
    st.error('Income can not be a negative value.')
#credit score to get interest rate
credit_test = st.number_input('What is your current credit score? (Used to calculate interest rate)', value = 650)
int_load_state = st.text('Calculating interest rate...')
int_rates = (list(np.linspace(32, 28.5, 629 - 300 + 1)) +
list(np.linspace(19.9, 17.8, 689 - 630 + 1)) +
list(np.linspace(15.5, 13.5, 719 - 690 + 1)) +
list(np.linspace(12.5, 10.3, 850 - 720 + 1)))
            #avg interest rates based on credit score
            #taken from https://www.bankrate.com/loans/personal-loans/average-personal-loan-rates/
#851 values for interest, one for each credit score 300 to 850
#input for model - int_test
if credit_test < 300:
    #if less than 300 credit score, max interest
    int_test = 36.0
else:
    int_test = int_rates[credit_test - 300]
    #a credit score of 300 will get int_rates[0]
st.text(f'Based on your credit score, your interest rate should be around {round(int_test, 2)}%')

#input for model - loan_percent_test
loan_percent_test = loan_amt/(income + .01) #no division by zero but income can be 0 so +.01


##modeling and getting the answer
input = [[int_test, loan_percent_test]]
pred = logreg.predict(input) #predict defaulting [1] - aka NOT paying, so not getting approved. 0 is approved/not default
prob = logreg.predict_proba(input) #predict possibility of defaulting and not defaulting
st.text(f'{pred}, {prob}')
