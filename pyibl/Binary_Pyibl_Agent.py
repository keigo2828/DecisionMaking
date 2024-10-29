from speedyibl import Agent 
import numpy as np
import random
import pandas as pd
import copy
import os
import optuna 
import plotly.io as pio

import time # to calculate time
#runs = 1000 # number of runs (participants)

#trials = 151 # number of trials (episodes)
average_p = [] # to store average of performance (proportion of maximum reward expectation choice)
average_time = [] # to save time 

def savelog(create_action_history,instance_history,last_choice):
  df = pd.DataFrame(create_action_history)
  df1 = pd.DataFrame(instance_history)
  df2 = pd.DataFrame(last_choice)

  df.to_csv("action_best.csv")
  df1.to_csv("instance_history_best.csv")
  df2.to_csv("last_history_best.csv")

def CreatData(Choice, Order, Slot, Slot_Result, P, Uid):
  actionlist = [[0]*32 for _ in range(int(len(Order)/32))]
  resultlist = [[0]*32 for _ in range(int(len(Order)/32))]
  #print('len',(len(Order)/32))
  #quit()

  for j in range(int(len(Order)/32)):
      for i in range(32):
          actionlist[j][i] = Slot[j*32 + i]
          resultlist[j][i] = Slot_Result[j*32 + i]
      CorrectActionList.append(Choice[j*32])
      #dfc = pd.DataFrame(CorrectActionList)
     # dfc.to_csv("dfc.csv")

  # 必要に応じて、返す変数を指定してください。ここでは例としてactionlistを返します。
  return actionlist, resultlist


def getdf():#データを取得
  cwd = os.getcwd()
  tmp = 'data/outputcsv_01.csv'
  path = os.path.join(cwd,tmp)
  df = pd.read_csv(path)
  Choice = df['Choice']
  Order = df['Order']
  Slot = df['Slot']
  Slot_Result = df['Slot_Result']
  P = df['P']
  Uid = df['User_id']
  #print(Choice, Order, Slot, Slot_Result, P, Uid)
  return Choice, Order, Slot, Slot_Result, P, Uid


Choice, Order, Slot, Slot_Result, P, Uid = getdf()

CorrectActionList = []

actionlist,resultlist = CreatData(Choice, Order, Slot, Slot_Result, P, Uid)
#print(actionlist)


#quit()

#実験のタスクの回数分runsを設定2990
runs = int(len(Order)/32) 



#choice = agent.choose(options)

create_action_history = [0]*runs
instance_history = [0]*runs
last_choice = [0]*runs
   

#その時のスロットマシンの確率。価値を更新する必要がないからいらないかも
#p = [0/8, 1/8, 2/8, 3/8, 4/8, 5/8, 6/8, 7/8, 8/8]
p = 1

# a_counts = 8
# b_counts = 32
# print(a_counts*(1-p))
# resulta = [1]*int(a_counts*p) + [0]*int(a_counts*(1-p))

# resultb = [1]*int(b_counts*p) + [0]*int(b_counts*(1-p))


# action_a = [options[0] for i in range(a_counts)]
# action_b = [options[1] for i in range(b_counts)]

# ct_ab = a_counts + b_counts

# #選択回数
ct_ab = 32

trials = ct_ab + 1
# trials = 33
# action_a.extend(action_b)
# print(options[0],options[1])
# quit()
# print(action_a)
# print(resulta,resultb)
# random.shuffle(action_a)

def colrate(SimuActionList,CorrectActionList):
  taskLength = len(SimuActionList)/9
  splitsim  = np.array_split(SimuActionList, 9)
  splitcorr = np.array_split(CorrectActionList, 9)
  y = 0
  for i in range(9):
      y += (sum(splitsim[i])/taskLength - sum(splitcorr[i])/taskLength)**2
  return y


def main(du,no,de):
  agent = Agent(default_utility = du, noise = no, decay = de, mismatchPenalty = None, outcome = True, lendeque = 250000)

  options = ['short','long'] 
  for r in range(runs,):
    pmax = []
    ttime = [0]
    agent.reset() #clear the memory for a new run  

    #作成した時系列行動結果とスロットマシンの結果をシャッフルする
    #設定のランダムな時系列で検証するため
    # random.shuffle(action_a)
    # random.shuffle(resulta)
    # random.shuffle(resultb)
    #どんな行動を選択したか記録する
    create_action_history[r] = copy.deepcopy(actionlist[r])

    a_ct = 0
    b_ct = 0



    for i in range(trials):     
      start = time.time()

      #
      if i >= ct_ab :
          choice = agent.choose(options) # choose one option from the list of two
      else:
          #時系列にある行動選択の結果を強制的に選択させる関数
          #choice =action_a[i]

          #actionlist[r][i] r回目のタスクのi番目試行
          #action short 0 action long 1
          if actionlist[r][i] == 0:
            choice = agent.forced_choice('short',options)
          else:
            choice = agent.forced_choice('long',options)

      # determine the reward that agent can receive
      # if choice == 'A':
      #   reward = 3


      # if random.random() <= 0.8:
      #   reward = -4
      # else:
      #   reward = 0
      # store the instance

        #最終選択
      if i >= ct_ab :

        #設定したスロットの当たり確率で報酬を取得
        if random.random() <= p:
          reward = 1
        else:
          reward = -1
      
      #選択がAの時
      elif choice ==  "short":
        #結果の報酬があるとき
        if resultlist[r][i] == "Win":
          reward = 1
          a_ct += 1
        #結果の報酬がない時
        else:
          reward = -1
          a_ct += 1
      #選択がBの時
      elif choice ==  "long":
        #結果の報酬がある時
        if resultlist[r][i]== "Win":
          reward = 1
          b_ct += 1
        #結果の報酬がない時
        else:
          reward = -1
          b_ct += 1



      agent.respond(reward)

      end = time.time()
      ttime.append(ttime[-1]+ end - start)
      pmax.append(choice == 'long') 
      #print(agent.utilitys)

    # print("????")
    last_choice[r] = choice
    if choice == "short":
      create_action_history[r].append(0)
    else:
      create_action_history[r].append(1)
      
    instance_history[r] = agent.instance_history
    average_p.append(pmax) # save performance of each run 
    average_time.append(ttime) # save time of each run

  end = time.time()

  #print(pd.DataFrame(create_action_history).shape)
  SimuActionList = np.array(create_action_history)[:,32]
  #df6 = pd.DataFrame(SimuActionList)
  #df6.to_csv("sim.csv")
  #return colrate(SimuActionList,CorrectActionList)
  savelog(create_action_history,instance_history,last_choice)


def objective(trial):

    default_utility = trial.suggest_float("default_utility", 1.0, 5.0)
    noise = trial.suggest_float("noise", 0, 1)
    decay = trial.suggest_float("decay", 0, 1)

    CorrectRate = main(default_utility,noise,decay)
    
    return CorrectRate

if __name__ == '__main__':
    print('started run')
    main(du = 1.011  ,no = 0.964,de = 0.644)

    #study = optuna.create_study(direction="maximize")
    # study = optuna.create_study(direction="minimize")
    # study.optimize(objective, n_trials=300)

    # trial = study.best_trial

    # print("Accuracy: {}".format(trial.value))
    # print("Best hyperparameters: {}".format(trial.params))
    # slice_fig = optuna.visualization.plot_slice(study)
    # contour_fig  = optuna.visualization.plot_contour(study, params=["default_utility", "noise", "decay"])
    # slice_fig.write_image("slice_plot.png")
    # contour_fig.write_image("contour_plot.png")

    print('finished run')

# import matplotlib.pyplot as plt
# import numpy as np 
# plt.rcParams["figure.figsize"] = (12,4)
# plt.subplot(int('12'+str(1)))
# plt.plot(range(trials+1), np.mean(np.asarray(average_time),axis=0), 'o-', color='darkgreen', markersize=2, linestyle='--', label='speedyIBL')
# plt.xlabel('Round')
# plt.ylabel('Time (s)')
# plt.title('Runing time')
# plt.legend()
# plt.subplot(int('12'+str(2)))
# plt.plot(range(trials), np.mean(np.asarray(average_p),axis=0), 'o-', color='darkgreen', markersize=2, linestyle='--', label='speedyIBL')
# plt.xlabel('Round')
# plt.ylabel('PMAX')
# plt.title('Performance')
# plt.legend()
# plt.grid(True)
# plt.show()