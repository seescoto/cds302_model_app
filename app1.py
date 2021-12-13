def app(): # group csv test
    import streamlit as st
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LogisticRegression
    from sklearn import metrics
    import matplotlib.pyplot as plt
    import numpy as np
    #app 1 - group guessing given a csv

    #title and stuff idk
    st.title('Credit Loan Risk')
    st.subheader('Enter a CSV file to determine loan approval')


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

        if len(dat.columns) != 2:
            st.warning('Please upload a CSV file with two columns')
        else: #go on regularly
            cols = ['interest_rate', 'loan_percent_income']
            new = []
            i = -1
            for c in dat.columns:
                i += 1
                if c != cols[i]: #if column names aren't correct
                    dat.columns = cols #replace first pair w/ col names
                    try: #if the column names are numbers, add to new
                        new.append(float(c))
                    except: #if not numbers, just go to next thing
                        break

            if new: #if we added to new, make it a df combine it with dat
                new = pd.DataFrame([new], columns = cols)
                dat = pd.concat([new, dat])


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
            
    st.header("For bugs encounters please contact us!")
    contact_form = """
    <form action="https://formsubmit.co/davis1kajuna@gmail.com" method="POST">
     <input type="hidden" name="_captcha" value="false">
     <input type="text" name="name" placeholder="Your name" required>
     <input type="email" name="email" placeholder="Your email" required>
     <textarea name="message" placeholder="Your message here."></textarea>
     <button type="submit">Send</button>
    </form>
    """
    
    st.markdown(contact_form, unsafe_allow_html=True)
    
    # Use Local CSS File
    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


    css_path = "style/style.css"
    local_css(css_path)
