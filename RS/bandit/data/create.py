import pandas as pd 
import numpy as np


df = pd.read_csv("outputcsv_01.csv")

data = np.zeros([244,9])

id = df["User_id"]
choice = df["Choice"]
order = df["Order"]
print(id[31])

# for j in range(9):
#     for i in range(244):
#         ind = id[i*31 + j * 244 ]
#         print(ind)
#         data[ind][j] = choice[i*31 + j * 244 ]
for  i in range(len(df)):
    if order[i] == 31:
        ind = id[i]
        print(ind)
        ct = int(i / (32*244) )
        data[ind][ct] = choice[i]


data = pd.DataFrame(data)   
data.to_csv("data.csv")