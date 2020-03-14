import pandas as pd
df = pd.read_csv('data1.txt', sep='\t', parse_dates=[0], usecols=[1,2,3])

from IPython import embed
embed()