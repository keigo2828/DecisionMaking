from speedyibl import Agent 
import numpy as np
import random
import pandas as pd
import copy

import time # to calculate time
runs = 1000 # number of runs (participants)
#trials = 151 # number of trials (episodes)
average_p = [] # to store average of performance (proportion of maximum reward expectation choice)
average_time = [] # to save time 


agent = Agent(default_utility=0)

options = ['A','B'] 

choice = agent.choose(options)

create_action_history = [0]*runs
instance_history = [0]*runs
last_choice = [0]*runs

a_counts = 8
b_counts = 32

action_a = [options[0] for i in range(a_counts)]
action_b = [options[1] for i in range(b_counts)]

ct_ab = a_counts + b_counts
trials = ct_ab + 1
action_a.extend(action_b)
#print(action_a)
random.shuffle(action_a)



for r in range(runs):
  pmax = []
  ttime = [0]
  agent.reset() #clear the memory for a new run
  

  random.shuffle(action_a)
  create_action_history[r] = copy.deepcopy(action_a)



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
    if random.random() <= 0.8:
      reward = -4
    else:
      reward = 0
    # store the instance
    agent.respond(reward)

    end = time.time()
    ttime.append(ttime[-1]+ end - start)
    pmax.append(choice == 'B') 
    print(agent.utilitys)
  print("????")
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