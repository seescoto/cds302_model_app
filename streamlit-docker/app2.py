###app 2 - individual guessing


import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy as np

#title and stuff idk
st.title('Credit Loan Risk')
st.subheader('Will you get approved for a loan?')


# data and model loading

#loading data - updated already
path = 'https://raw.githubusercontent.com/seescoto/cds303_model_app/main/updated_csv.csv'
credit_risk = pd.read_csv(path)
Feature_cols = ['interest_rate', 'loan_percent_income']


#fitting the model
#setting x and y
X = credit_risk[Feature_cols]
y = credit_risk.loan_status
#split into test/train sets - no randomness so same results each time
X_train,X_test,y_train,y_test = train_test_split(X, y, test_size=0.20, random_state = 0)
#creating model and fitting it
logreg = LogisticRegression()
logreg.fit(X_train, y_train)
#y_pred = logreg.predict(X_test)

#model and data fitted!


#describe interest rate stuff for looking at it idk
#st.text(credit_risk['interest_rate'].describe())


###use inputs in sidebar

#loan amount
#st.sidebar.text()

loan_amt = st.sidebar.number_input('How much money would you like to loan in dollars?', value = 10000)
if loan_amt <= 0:
    st.warning('Loan amount must be a positive non-zero value.')

#income
income = st.sidebar.number_input('What is your annual income in dollars?', value = 50000)
if income < 0:
    st.warning('Income can not be a negative value.')

#loan percent interest calculated from above
loan_percent_test = loan_amt/(income + 0.01) #so no dividing by 0 even if income is 0

#interest rate
opts = ['Yes, I know my interest rate',
'No, please estimate for me']

ints = st.sidebar.selectbox(
'Do you know what interest rate you would be approved for if given a loan?', opts)

if ints == opts[0]: #if they know their interest rate
    int_test = st.sidebar.number_input('Please enter the interest rate you were previously approved for:',
    value = 12.00)
elif ints == opts[1]: #if they dont know
    #credit score to estimate interest rate
    #the bank gives an interest rate and a random person might not know what theirs would be
    #so we'll just give them one based off an educated guess
    credit_test = st.sidebar.number_input('What is your current credit score?',
    value = 600)
    if credit_test < 0 or credit_test > 850:
        st.warning('Credit score must be an integer between 0 and 850.')
    int_rates = (list(np.linspace(20.58, 17.12, 500 - 300 + 1)) +
    list(np.linspace(17.11, 10.5, 600 - 501 + 1)) +
    list(np.linspace(10.49, 5.5, 660 - 601 + 1)) +
    list(np.linspace(5.49, 3.67, 780 - 661 + 1)) +
    list(np.linspace(3.66, 3.66, 850 - 781 + 1)))
                #avg interest rates based on credit score
                #https://www.businessinsider.com/personal-finance/average-auto-loan-interest-rate
                #closest to credit_risk['interest_rate'].describe() stats
    #851 values for interest, one for each credit score 300 to 850
    #input for model - int_test
    if credit_test < 300:
        #if less than 300 credit score, max interest
        int_test = 36.0
    else:
        int_test = int_rates[credit_test - 300]
    st.sidebar.caption(f'Based on your credit score, your interest rate should be around {round(int_test, 2)}%')
    st.sidebar.caption('Estimations of interest rate based on credit score may not yield accurate results.')
else:
    st.warning(f'Please enter either your interest rate or credit score')




##modeling and getting the answer after checkbox has been selected
input = [[int_test, loan_percent_test]]
pred = logreg.predict(input) #predict defaulting [1] - aka NOT paying. 0 is approved/not default
prob = logreg.predict_proba(input) #predict possibility of not defaulting and not defaulting
if pred == 0:
    st.text(f'Our model predicts you will get approved for a loan!')
    st.text(f'The probability that you will be approved is {round(prob[0][0]*100, 2)}%')
else:
    st.text(f'Our model predicts that you will not get approved for a loan.')
    st.text(f'The probability that you will be approved is {round(prob[0][0]*100, 2)}%')
