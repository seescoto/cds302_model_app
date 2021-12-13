#Written in Python 3.10
#Deps
import dash
from dash import dcc
from dash import html
#from google.colab import files
import io
import plotly.express as px
import pandas as pd
import statistics
import statistics
import numpy as np
import plotly.graph_objects as go

#Import our dataset
df = pd.read_csv('credit_risk_dataset.csv')


#Counters to count the number of defaulters and non defaulters for each category of home ownership
#Rent without default
r_0 = 0
#Rent and we defaulted
r_1 = 0
#Mortgage no default
m_0 = 0
#Mortgage and default
m_1 = 1
#Ownership and no defaults
o_0 = 0
#Ownership of house and we defaulted
o_1 = 0
#Other with no defaults
ot_0 = 0
#Other with defaults
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

#Creating totals of each wealth category 
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





def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ], className="Table")

app = dash.Dash(__name__)

colors = {
    "background": "#393A3B",
    "text": "#E6E9EC"
}

fig1 = px.bar(x=income_dict.keys(), y=income_dict.values())
fig2 = px.bar(df, x=df["loan_intent"].head(5000), y=df["loan_amnt"].head(5000), color=df["loan_grade"].head(5000), barmode="group")
fig3 = px.histogram(df, x=df["person_home_ownership"], barmode="group", color=df["loan_status"])
fig4 = px.histogram(df, x=df["person_age"], barmode="group", color=df["loan_status"], nbins = 20)
fig5 = px.scatter(x=df["person_income"].head(100), y=df["loan_amnt"].head(100), title="Income against loan amount")

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

# fig = px.bar(x=loan_group, y=count, barmode="group")

fig1.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig3.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

fig4.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
),

fig5.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)


app.layout = html.Div([
    html.Div([
        html.H1("Group 4: To Lend Or Not To Lend")
        ], className="heading"),
    
    html.Div([
         html.H1(children='Credit Risk Dataset Table'),
    generate_table(df)
        ],className="float-child"),
    
    
    html.Div([
         html.Div([
        html.H1("Part 1: Data Visualization.")
        ], className="heading"),
        
        
        html.H1("Income brackets"),
        dcc.Graph(id="income", figure=fig1)
        
    ], className="float-child"),
    
      html.Div([
            html.H3(["Income brackets which show the division of groups in the following brackets", html.Br(), "Low income : $32,048 or less", html.Br(),"Lower-middle class	: $32,048 - $53,413", html.Br(),"Middle class	: $53,413 - $106,827", html.Br(),"Upper-middle class	: $106,827 - $373,894", html.Br(),"Rich	: $373,894 and up"])
            ], className="float-child"),

    
    
    html.Div([
        html.H1("Loan Intent"),
        dcc.Graph(id="intent", figure=fig2)

    ], className="float-child"),
    
     html.Div([
        html.H1("Home ownership loan status"),
        dcc.Graph(id="home", figure=fig3)

    ], className="float-child"),
     
     html.Div([
        html.H1("Home ownership loan status"),
        dcc.Graph(id="age_loan_status", figure=fig4)

    ], className="float-child"),
     
      html.Div([
        html.H1("Loan Default status"),
        dcc.Graph(id="loan_status", figure=fig)

    ], className="float-child"),
      
        html.Div([
        html.H1("Income against loan amount"),
        dcc.Graph(id="income_vs_loan", figure=fig5)

    ], className="float-child")

], className="float-container")




if __name__ == "__main__":
    app.run_server(host='0.0.0.0',debug=True, use_reloader=False)


