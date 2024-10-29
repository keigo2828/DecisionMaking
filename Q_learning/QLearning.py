import numpy as np
import

class QLearning:

    def __init__(self, arm_id, alpha, beta):
        self.arm_num = arm_id
        self.Q_value = np.zeros(self.arm_num)
        self.select_bandit_id = 0
        self.alpha = alpha
        self.beta = beta

        

    def reset(self):
        self.Q_value = np.zeros(self.arm_num)


    def update(self,reward,t,s):
        self.Q_value[self.select_bandit_id]  +=  (reward - self.Q_value[self.select_bandit_id]) / (self.bandit_ct[self.select_bandit_id] + 1)

    def softmax(self):
        u = sum(np.exp(self.beta*self.Q_value))
        return np.exp(self.beta*self.Q_value)/u
        

    def select_action(self):

        y = self.softmax()
        
        self.select_bandit_id = action_id


