import numpy as np
import random

class RescorlaWagner:

    def __init__(self,arm_id,trials,steps,alpha,beta):
        self.arm_num = arm_id
        self.action_space = [0,1]
        self.Value = np.zeros(self.arm_num)
        self.select_bandit_id = 0
        self.bandit_ct = np.zeros(self.arm_num)
        self.action_history = np.zeros((trials, steps))
        self.alpha = alpha
        self.beta = beta
        

    def reset(self):
        self.Value = np.zeros(self.arm_num)
        self.bandit_ct = np.zeros(self.arm_num)


    def update(self,reward,t,s):
        self.bandit_ct[self.select_bandit_id] += 1
        self.Value[self.select_bandit_id]  +=  (reward - self.Value[self.select_bandit_id]) / (self.bandit_ct[self.select_bandit_id] + 1)
        self.action_history[t][s] = int(self.select_bandit_id)

    def choice_update(self,reward,t,s,action):
        self.bandit_ct[action] += 1
        self.Value[action]  +=  (reward - self.Value[action]) / (self.bandit_ct[action] + 1)
        self.action_history[t][s] = int(action)

    def update_larning_rate(self,reward,t,s):
        self.bandit_ct[self.select_bandit_id] += 1
        self.Value[self.select_bandit_id]  =  (self.alpha * reward) + ((1 - self.alpha ) *  self.Value[self.select_bandit_id])
        self.action_history[t][s] = int(self.select_bandit_id)

    def choice_update_larning_rate(self,reward,t,s,action):
        self.bandit_ct[action] += 1
        self.Value[action]  =  self.alpha * reward + (1 - self.alpha ) *  self.Value[self.select_bandit_id]
        self.action_history[t][s] = int(action)

        

    def select_action(self,ct):
        if ct ==0:
            r = random.random()
            if r <= 0.5:
                action_id = 0
            else:
                action_id = 1
        else:
            #action_id = self.max()
            action_id  = self.softmax()
            
            self.select_bandit_id = action_id
        return action_id

    def softmax(self):
        u = sum(np.exp(self.beta*self.Value))
        #print(u)
        p = np.exp(self.beta*self.Value)/u
        action_id = np.random.choice(self.action_space,p=p)
        return action_id

    def max(self):
        action_id = np.argmax(self.Value)
        return action_id
    