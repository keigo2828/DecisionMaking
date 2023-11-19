import numpy as np
import random

class RS:

    def __init__(self,arm_id,level,trials,steps):
        self.arm_num = arm_id
        self.rs_value = np.zeros(self.arm_num)
        self.aspiration_level = level
        self.expected_value = np.zeros(self.arm_num)
        self.select_bandit_id = 0
        self.bandit_ct = np.zeros(self.arm_num)
        self.action_history = np.zeros((trials, steps))
        

    def reset(self):
        self.rs_value = np.zeros(self.arm_num)
        self.expected_value = np.zeros(self.arm_num)
        self.bandit_ct = np.zeros(self.arm_num)


    def update(self,reward,t,s):
        self.bandit_ct[self.select_bandit_id] += 1
        reliability =  self.bandit_ct[self.select_bandit_id] / np.sum(self.bandit_ct)
        self.expected_value[self.select_bandit_id]  +=  (reward - self.expected_value[self.select_bandit_id]) / (self.bandit_ct[self.select_bandit_id] + 1)
        self.rs_value[self.select_bandit_id] = reliability * (self.expected_value[self.select_bandit_id] - self.aspiration_level) 
        self.action_history[t][s] = int(self.select_bandit_id)

    def choice_update(self,reward,t,s,action):
        self.bandit_ct[action] += 1
        reliability =  self.bandit_ct[action] / np.sum(self.bandit_ct)
        self.expected_value[action]  +=  (reward - self.expected_value[action]) / (self.bandit_ct[action] + 1)
        self.rs_value[action] = reliability * (self.expected_value[action] - self.aspiration_level) 
        self.action_history[t][s] = int(action)

        

    def select_action(self,ct):
        if ct ==0:
            r = random.random()
            if r <= 0.5:
                action_id = 0
            else:
                action_id = 1
        else:
            action_id = np.argmax(self.rs_value)
            self.select_bandit_id = action_id
        return action_id
        