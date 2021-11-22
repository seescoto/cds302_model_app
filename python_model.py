# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 09:02:16 2021

@author: davis
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.preprocessing import StandardScaler


st.title("CREDIT RISK: Loan default model")
st.subheader("This model will predict if a customer is likely to default a loan or not")



#Read Dataframe
path = "/content/credit_risk_dataset.csv"
df = pd.read_csv(path)


#Drop categorical columns
credit_risk = df.select_dtypes(exclude=['object'])

#Renaming columns
credit_risk.columns = ['age', 'income', 'employment_length', 'amount', 'interest_rate', 'loan_status', 'loan_percent_income', 'credit_length']


#Mean imputation on interest_rate column
credit_risk["interest_rate"].fillna(credit_risk["interest_rate"].mean(), inplace = True) 

#Creating a correlation heatmap
fig = plt.figure(figsize = (12,10))
cor = credit_risk.corr()
sns.heatmap(cor, annot = True, cmap=plt.cm.Reds)
plt.title("Correlation heatmap between Feature columns and target columm")
plt.show()
st.pyplot(fig)

#Checking correlation between target column and feature columns
cor_target = abs(cor['loan_status'])
relevant_features = cor_target[cor_target>0.3]
print(relevant_features)
print(credit_risk[["interest_rate","loan_percent_income"]].corr())

#splitting dataset into features and target variables
Feature_cols = ['interest_rate', 'loan_percent_income']

X = credit_risk[Feature_cols]
y = credit_risk.loan_status

#Splitting target column and feature columns into training and testing sets
X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.20, random_state = 0)


#Creating an object from LogisticRegression class
logreg = LogisticRegression()

#Fitting the model with data
logreg.fit(X_train, y_train)
y_pred = logreg.predict(X_test)

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


print("Accuracy:",metrics.accuracy_score(y_test, y_pred))
print("Precision:",metrics.precision_score(y_test, y_pred))
print("Recall:",metrics.recall_score(y_test, y_pred))


y_pred_proba = logreg.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba)
auc = metrics.roc_auc_score(y_test, y_pred_proba)
fig, ax1 = plt.subplots()
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)
plt.title("Receiver operating characteristic (ROC curve)")
plt.show()
st.pyplot(fig)

name = st.text_input("Name of customer.")
loan_pct_income = st.number_input("Loan percentage income")
int_rate = st.number_input("Interest rate")

int_rate, loan_pct_income = 0, 0



input_data = [[int_rate, loan_pct_income]]
prediction = logreg.predict(input_data)
predict_probability = logreg.predict_proba(input_data)

if prediction[0] == 1:
	st.subheader('{} is likely to default loan with a probability of {}%'.format(name , round(predict_probability[0][1]*100 , 2)))
else:
	st.subheader(' {} is likely not to default loan with a probability of {}%'.format(name, round(predict_probability[0][0]*100 , 2)))
