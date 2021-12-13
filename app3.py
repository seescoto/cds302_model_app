def app(): #create random test values
    import streamlit as st
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn import metrics
    import numpy as np
    import matplotlib.pyplot as plt


    st.title('Credit Loan Risk')
    st.subheader('Randomize application values and test them!')


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

    #after inputting size, make df
    #X is already defined as credit_risk[feature columns] so can use that

    lmin = X['loan_percent_income'].min()
    lmax = X['loan_percent_income'].max()
    irmin = X['interest_rate'].min()
    irmax = X['interest_rate'].max()

    #how big should df be?
    size = st.number_input('How many applications would you like to evaluate?', value = 500)
    if size <= 0:
        st.warning('Can not test less than one sample at a time')
    else:
        #random list of interests based on stats
        intlist = (irmax - irmin) * np.random.random_sample(size) + irmin
        #randome lists of loan percents based on stats
        lpilist = (lmax - lmin) * np.random.random_sample(size) + lmin

        #making lists into a dict, then putting dict into df
        d = {'interest_rate': intlist, 'loan_percent_income':lpilist}
        dat = pd.DataFrame(d)

        st.text('Calculating...')

        loans = logreg.predict(dat)
        probs = logreg.predict_proba(dat)[:, 0]
        dat['loan_approved'] = loans
        dat['prob_of_approval'] = probs

        repdict = {1 : 'Denied', 0: 'Approved'}


        dat['loan_approved'] = dat['loan_approved'].map(repdict)

        st.write(dat)

        #put in a plot of values approved or not


        fig = plt.figure()

        groups = dat.groupby("loan_approved")
        for name, group in groups:
            plt.plot(group["interest_rate"], group["loan_percent_income"] * 100,
            marker = 'o', linestyle=" ", label=name)
        plt.legend()
        plt.title('Loan Applications Approved/Denied')
        plt.xlabel('Interest rate for loan')
        plt.ylabel('Loan is ___ percent of income')

        st.pyplot(fig)
        
        
