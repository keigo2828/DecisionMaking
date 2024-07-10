from speedyibl import Agent 
import numpy as np
import random
import pandas as pd
import copy
import os

import time # to calculate time
runs = 1000 # number of runs (participants)
#trials = 151 # number of trials (episodes)
average_p = [] # to store average of performance (proportion of maximum reward expectation choice)
average_time = [] # to save time 


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
  return Choice, Order, Slot, Slot_Result, P, Uid


def CreatData():
  #for i in  range(32):
  #  resultshort = 
  #  resultlong =
  pass


agent = Agent(default_utility=1.8)

options = ['A','B'] 
choice = agent.choose(options)

create_action_history = [0]*runs
instance_history = [0]*runs
last_choice = [0]*runs
   

p = 0.5

a_counts = 8
b_counts = 32
print(a_counts*(1-p))
resulta = [1]*int(a_counts*p) + [0]*int(a_counts*(1-p))

resultb = [1]*int(b_counts*p) + [0]*int(b_counts*(1-p))


action_a = [options[0] for i in range(a_counts)]
action_b = [options[1] for i in range(b_counts)]

ct_ab = a_counts + b_counts

#ct_ab = 32

trials = ct_ab + 1
#trials = 33
action_a.extend(action_b)
print(options[0],options[1])
print(action_a)
print(resulta,resultb)
random.shuffle(action_a)



for r in range(runs):
  pmax = []
  ttime = [0]
  agent.reset() #clear the memory for a new run  

  random.shuffle(action_a)
  random.shuffle(resulta)
  random.shuffle(resultb)

  create_action_history[r] = copy.deepcopy(action_a)

  a_ct = 0
  b_ct = 0

  for i in range(trials):     
    start = time.time()

    if i >= ct_ab :
        choice = agent.choose(options) # choose one option from the list of two
    else:
        #choice =action_a[i]
        choice = agent.forced_choice(action_a[i],options)

    # determine the reward that agent can receive
    # if choice == 'A':
    #   reward = 3


    # if random.random() <= 0.8:
    #   reward = -4
    # else:
    #   reward = 0
    # store the instance

    if i >= ct_ab :
      if random.random() <= p:
        reward = 1
      else:
        reward = -1
    elif choice ==  "A":
      if resulta[a_ct] == 1:
         reward = 1
         a_ct += 1
      else:
         reward = -1
         a_ct += 1
    elif choice ==  "B":
      if resultb[b_ct] == 1:
         reward = 1
         b_ct += 1
      else:
         reward = -1
         b_ct += 1



    agent.respond(reward)

    end = time.time()
    ttime.append(ttime[-1]+ end - start)
    pmax.append(choice == 'B') 
    print(agent.utilitys)

  # print("????")
  last_choice[r] = choice
     
  instance_history[r] = agent.instance_history
  average_p.append(pmax) # save performance of each run 
  average_time.append(ttime) # save time of each run

end = time.time()

df1 = pd.DataFrame(instance_history)
df = pd.DataFrame(create_action_history)
df2 = pd.DataFrame(last_choice)

df.to_csv("action.csv")
df1.to_csv("instance_history.csv")
df2.to_csv("last_history.csv")









import matplotlib.pyplot as plt
import numpy as np 
plt.rcParams["figure.figsize"] = (12,4)
plt.subplot(int('12'+str(1)))
plt.plot(range(trials+1), np.mean(np.asarray(average_time),axis=0), 'o-', color='darkgreen', markersize=2, linestyle='--', label='speedyIBL')
plt.xlabel('Round')
plt.ylabel('Time (s)')
plt.title('Runing time')
plt.legend()
plt.subplot(int('12'+str(2)))
plt.plot(range(trials), np.mean(np.asarray(average_p),axis=0), 'o-', color='darkgreen', markersize=2, linestyle='--', label='speedyIBL')
plt.xlabel('Round')
plt.ylabel('PMAX')
plt.title('Performance')
plt.legend()
plt.grid(True)
plt.show()