import pandas as pd

df = pd.Series([1,2,3],index=['a','b','c'])
df1 = pd.Series([4,5])
df1.index = ['d','e']
df = df.append(df1)
print(df)