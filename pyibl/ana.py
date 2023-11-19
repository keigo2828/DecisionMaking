import pandas as pd

df = pd.read_csv("last_history.csv")
df = df.replace("A",0)
df = df.replace("B",1)
print(df.mean())
