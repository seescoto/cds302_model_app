#workout for app


#MULTIPLE PAGES
#FROM https://medium.com/@u.praneel.nihar/
#building-multi-page-web-app-using-streamlit-7a40d55fa5b4

#app.py
import app1
import app2
import streamlit as st
PAGES = {
    "App1": app1,
    "App2": app2
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
