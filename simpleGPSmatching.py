import pandas as pd
data = pd.read_csv('data1.txt',sep='\t',parse_dates=[1],usecols=[1,2,3])
from IPython import embed
embed()