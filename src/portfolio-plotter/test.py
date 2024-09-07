import pandas as pd

df = pd.read_csv('../data/BuyandHold_EQL_DOLLAR_pnl.csv')

print(df.to_dict(orient='records'))