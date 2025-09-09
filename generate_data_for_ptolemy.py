import pandas as pd

try:
	df1 = pd.read_csv('raw_data/F02_U09_R01_data.csv')
except FileNotFoundError:
	raise FileNotFoundError('Run generate_raw_data_csv.py first')

df_adl = df1[df1['label'] == 'ADL']
l = [df_adl.copy()] * 100

df_bho = pd.concat([df1] + l, axis=0).dropna().reset_index(drop=True)
df_bho.to_csv('ADL_fall_raw_signal.csv', index=False)
