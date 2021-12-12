# -*- coding: utf-8 -*-
"""
Created on Fri Dec 10 20:34:59 2021

@author: davis
"""

import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def app():

    st.header("MODEL PERFORMANCE VISUALIZATIONS")

    #loading data
    path = 'https://raw.githubusercontent.com/seescoto/cds303_model_app/main/updated_csv.csv'
    credit_risk = pd.read_csv(path)
    Feature_cols = ['interest_rate', 'loan_percent_income']

    fig = plt.figure(figsize = (12,10))
    cor = credit_risk.corr()
    sns.heatmap(cor, annot = True, cmap=plt.cm.Reds)
    plt.title("Correlation heatmap between Feature columns and target columm")
    plt.show()
    st.pyplot(fig)

    #fitting the model
    #setting x and y
    X = credit_risk[Feature_cols]
    y = credit_risk.loan_status
    #split into test/train sets - no randomness so same results each time
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.20, random_state = 0)
    #creating model and fitting it
    logreg = LogisticRegression()
    logreg.fit(X_train, y_train)
    y_pred = logreg.predict(X_test)


    y_pred_proba = logreg.predict_proba(X_test)[::,1]
    fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
    auc = metrics.roc_auc_score(y_test, y_pred_proba)
    fig, ax1 = plt.subplots()
    plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
    plt.legend(loc=4)
    plt.title("Receiver operating characteristic (ROC curve)")
    plt.show()
    st.pyplot(fig)

    cnf_matrix = metrics.confusion_matrix(y_test,y_pred)
    print(cnf_matrix)

    class_names=[0,1]
    fig, ax = plt.subplots()
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names)
    plt.yticks(tick_marks, class_names)
    # create heatmap
    sns.heatmap(pd.DataFrame(cnf_matrix), annot=True, cmap="YlGnBu" ,fmt='g')
    ax.xaxis.set_label_position("top")
    plt.tight_layout()
    plt.title('Confusion matrix', y=1.1)
    plt.ylabel('Actual label')
    plt.xlabel('Predicted label')
    plt.show()
    st.pyplot(fig)

    st.header("For bugs encounters please contact me!")
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


    local_css("style.css")
