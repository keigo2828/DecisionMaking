import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import os

def read(str):
    df  = pd.read_csv(str)
    return df

def plot_selection_rate(df):
    df = df.iloc[:, -1]
    se = pd.Series(df)
    a = pd.Series.value_counts(se)
   # print(a.sort_index())
    a = a.sort_index() 
    left = np.array(["bandit0","bandit1"])
    height  = np.array(a)
    plt.bar(left,height,align="center")
    path = os.getcwd()
    str = path + "/png/{0.6}{0.6}".format() 
    os.mkdir(str,exit = True)
    plt.savefig()
    plt.show()
    

def main():
    df = read("log/free_action_sequence_p(0.6,0.6)aleph0.5.csv")
    plot_selection_rate(df)

    
if __name__ == '__main__':
    print('started run')
    main()
    print('finished run')