#MULTIPLE PAGES
#FROM https://medium.com/@u.praneel.nihar/
#building-multi-page-web-app-using-streamlit-7a40d55fa5b4
#!pip install seaborn

import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy as np
import csv
import seaborn as sns


#cheat sheet for adding the visualization page
#make your python file and then name it something like vis.py
#(or change it and change code)
#put your entire code inside a function defining app
#so like def app():
#then an indent and ur entire code for the page
#and import vis and then uncomment the visualizations part of the dict


import app1
import app2
import vis
import streamlit as st
PAGES = {
    "Evaluate 1 loan application at a time": app2,
    "Evaluate multiple applications (CSV)": app1,
    "Visualizations" : vis
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
