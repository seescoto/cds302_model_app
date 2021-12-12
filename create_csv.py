#create random input csv

import numpy as np
import pandas as pd

#getting min and max values for columns from og data
path = 'https://raw.githubusercontent.com/seescoto/cds303_model_app/main/updated_csv.csv'
df = pd.read_csv(path)
lmin = df['loan_percent_income'].min()
lmax = df['loan_percent_income'].max()
irmin = df['interest_rate'].min()
irmax = df['interest_rate'].max()

#can be changed, length of test csv
size = 1000

#random list of interests based on stats
intlist = (irmax - irmin) * np.random.random_sample(size) + irmin

#randome lists of loan percents based on stats
lpilist = (lmax - lmin) * np.random.random_sample(size) + lmin


#making lists into a dict, then putting dict into df
d = {'interest_rate': intlist, 'loan_percent_interest':lpilist}
df2 = pd.DataFrame(d)

df2.to_csv('test.csv')
