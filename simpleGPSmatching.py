import pandas as pd
df = pd.read_csv('data1.txt', sep='\t', parse_dates=[0], usecols=[1,2,3])
df.insert(0, 'uuid', [1]*len(df))


from IPython import embed
embed()