# -*- coding: utf-8 -*-
"""
Created on Sun Dec 12 22:56:58 2021

@author: davis
"""

def app():
    import plotly.express as px
    import pandas as pd
    import statistics
    import numpy as np
    import plotly.graph_objects as go
    import streamlit as st
    import time
    
    my_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)
     
    with st.spinner('Wait for it...'):
        time.sleep(25)
    st.success('Done!')
    
    
    
    
    
    path = "credit_risk_dataset.csv"
    
    df = pd.read_csv(path)
    r_0 = 0
    r_1 = 0
    m_0 = 0
    m_1 = 1
    o_0 = 0
    o_1 = 0
    ot_0 = 0
    ot_1 = 0
    
    
    ho = dict(df['person_home_ownership'].value_counts())
    tot = 0
    for key, value in ho.items():
        tot += value
    
    for i in range(len(df)):
        if df.iloc[i]['person_home_ownership'] == "RENT" and df.iloc[i]['loan_status'] == 0:      
            r_0 += 1
        elif df.iloc[i]['person_home_ownership'] == "RENT" and df.iloc[i]['loan_status'] == 1:      
            r_1 += 1
        elif df.iloc[i]['person_home_ownership'] == "MORTGAGE" and df.iloc[i]['loan_status'] == 0: 
            m_0 += 1
        elif df.iloc[i]['person_home_ownership'] == "MORTGAGE" and df.iloc[i]['loan_status'] == 1:
            m_1 += 1   
        elif df.iloc[i]['person_home_ownership'] == "OWN" and df.iloc[i]['loan_status'] == 0:
            o_0 += 1
        elif df.iloc[i]['person_home_ownership'] == "OWN" and df.iloc[i]['loan_status'] == 1:
            o_1 += 1
        elif df.iloc[i]['person_home_ownership'] == "OTHER" and df.iloc[i]['loan_status'] == 0:  
            ot_0 += 1
        else:  
            ot_1 += 1
    
    
    for i in range(len(df["person_age"])):
        if df["person_age"][i] >= 95:
            df["person_age"][i] = statistics.mean(df["person_age"])
    
    
    low_income = 0
    lower_middle = 0
    middle_class= 0
    upper_middle = 0
    rich = 0
    for i in df["person_income"]:
        if i <= 32048:
            low_income += 1
        elif i > 32048 and i <= 53413:
            lower_middle += 1
        elif i > 53413 and i <= 106827:
            middle_class += 1
        elif i > 106827 and i <= 373894:
            upper_middle += 1
        else:
            rich += 1
    
    income_dict = {
    "low_income" : low_income,
    "lower_middle" : lower_middle,
    "middle_class" : middle_class,
    "upper_middle" : upper_middle,
    "rich" : rich
    }
    
    loan_status_dict = {}
    df['loan_status'].value_counts()
    
    
    

    
    fig1 = px.bar(x=income_dict.keys(), y=income_dict.values())
    fig1.update_layout(width=800)
    fig2 = px.bar(df, x=df["loan_intent"].head(5000), y=df["loan_amnt"].head(5000), color=df["loan_grade"].head(5000), barmode="group")
    fig2.update_layout(width=800)
    fig3 = px.histogram(df, x=df["person_home_ownership"], barmode="group", color=df["loan_status"])
    fig3.update_layout(width=800)
    fig4 = px.histogram(df, x=df["person_age"], barmode="group", color=df["loan_status"], nbins = 20)
    fig4.update_layout(width=800)
    fig5 = px.bar(df, x=df['loan_int_rate'], y = df['loan_status'])
    fig5.update_layout(width=800)
    fig6 = px.bar(df, x=df['loan_percent_income'], y=df['loan_amnt'], color=df['loan_status'])
    fig6.update_layout(width=800)
    
    labels = ["RENT","OWN","MORTGAGE","OTHERS"]
    
    widths = np.array([ho["RENT"]/tot*100,ho["OWN"]/tot*100,ho["MORTGAGE"]/tot*100,ho["OTHER"]/tot*100])
    
    data = {
    "DEFAULT": [r_1/(r_1+r_0)*100,o_1/(o_1+o_0)*100,m_1/(m_1+m_0)*100,ot_1/(ot_1+ot_0)*100],
    "NON DEFAULT": [r_0/(r_1+r_0)*100,o_0/(o_1+o_0)*100,m_0/(m_1+m_0)*100,ot_0/(ot_1+ot_0)*100]
    }
    
    fig = go.Figure()
    for key in data:
        fig.add_trace(go.Bar(
            name=key,
            y=data[key],
            x=np.cumsum(widths)-widths,
            width=widths,
            offset=0,
            customdata=np.transpose([labels, widths*data[key]]),
            texttemplate="%{y}%",
            textposition="inside",
            textangle=0,
            textfont_color="white",
            hovertemplate="<br>".join([
            "label: %{customdata[0]}",
            "width: %{width}",
            "height: %{y}",
            "area: %{customdata[1]}",
        ])
    ))
        
    colors = {
    "background": "#393A3B",
    "text": "#E6E9EC"
}
    
    fig.update_xaxes(
    tickvals=np.cumsum(widths)-widths/2,
    ticktext= ["%s<br>%d" % (l, w) for l, w in zip(labels, widths)]
    )
    
    fig.update_xaxes(range=[0,100])
    fig.update_yaxes(range=[0,100])
    
    fig.update_layout(
    title_text="Marimekko Chart on loan defaulters",
    barmode="stack",
    uniformtext=dict(mode="hide", minsize=10),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )
   
    
    st.write(fig1)
    st.write(fig2)
    st.write(fig3)
    st.write(fig4)
    st.write(fig5)
    st.write(fig6)
    st.write(fig)
    
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


    css_path = "style/style.css"
    local_css(css_path)
