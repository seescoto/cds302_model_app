#app 1 - group guessing given a csv

import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy as np
from sklearn import *
import csv

#title and stuff idk
st.title('Credit Loan Risk')
st.subheader('Will you get approved for a loan?')


# data and model loading

#loading data
path = 'https://raw.githubusercontent.com/seescoto/cds303_model_app/main/updated_csv.csv'
credit_risk = pd.read_csv(path)
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
#y_pred = logreg.predict(X_test)

#model and data fitted!


#describe interest rate stuff for looking at it idk
#st.text(credit_risk['interest_rate'].describe())


###use inputs in sidebar


dat = st.sidebar.file_uploader('Please upload the data in CSV form', type = 'csv')
caps = ['Your CSV file should have two columns.',
"The first one should represent the interest rate for the given loan, and the second should represent what percentage of said person's income is their requested loan.",
'E.G. if they make $50,000 and want a loan of $10,000, their loan percent income would be 10,000/50,000 = 1/5 = 0.2',
'example row for a loan that is 20% of the income with a 15% interest rate: 15, .2']

for i in caps:
    st.sidebar.caption(i)

if dat != None:

    dat = pd.read_csv(dat, sep = ',')
    cols = ['interest_rate', 'loan_percent_income']
    new = []
    i = -1
    for c in dat.columns:
        i += 1
        if c != cols[i]: #if column names aren't correct
            dat.columns = cols #replace first pair w/ col names
            try: #if the column names are numbers, add to new
                new.append(float(c))
            except: #if not numbers, tell them we changed them
                break

    if new: #if we added to new, make it a df combine it with dat
        new = pd.DataFrame([new], columns = cols)
        dat = pd.concat([new, dat])




    st.write(dat)
    st.text('Calculating...')

    loans = []
    probs = []

    for i in range(len(dat)): #for all rows
        input = [[dat.iloc[i][0], dat.iloc[i][1]]]
        st.text(input)
        pred = logreg.predict(input)
        prob = logreg.predict_proba(input)[:, 0]
        loans.append(pred)
        probs.append(prob)

    dat['Loan'] = loans
    dat['Probability'] = probs

    ##modeling and getting the answer after checkbox has been selected
    #for i in dat.columns:
        #input = dat.
    dat['Loan'] = logreg.predict(dat) #predict defaulting [1] 0 is approved/not default
    st.write(logreg.predict(dat))
    dat['Probability'] = logreg.predict_proba(dat)[:,0] #predict possibility of not defaulting and not defaulting


    st.write(dat)
