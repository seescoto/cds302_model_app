def app():
    import streamlit as st
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn import metrics
    import numpy as np
    #app 1 - group guessing given a csv

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


    dat = st.file_uploader('Please upload the data in CSV form', type = 'csv')
    caps = ['Your CSV file should have two columns.',
    "The first one should represent the interest rate for the given loan, and the second should represent what percentage of said person's income is their requested loan.",
    'E.G. if they make $50,000 and want a loan of $10,000, their loan percent income would be 10,000/50,000 = 1/5 = 0.2',
    'example row for a loan that is 20% of the income with a 15% interest rate: 15, .2']

    for i in caps:
        st.caption(i)

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





        loans = logreg.predict(dat)
        probs = logreg.predict_proba(dat)[:, 0]
        st.text(loans)
        dat['loan_approved'] = loans
        dat['prob_of_approval'] = probs



        st.write(dat)
