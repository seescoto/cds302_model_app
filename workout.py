#workout for app


#MULTIPLE PAGES
#FROM https://medium.com/@u.praneel.nihar/
#building-multi-page-web-app-using-streamlit-7a40d55fa5b4

import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
import numpy as np
import csv

#app.py
import app12
import app22
import streamlit as st
PAGES = {
    "Evaluate 1 at a time": app22,
    "Upload a file to Evaluate": app12
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
