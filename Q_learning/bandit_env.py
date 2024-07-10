import random

class Bandit:
    
    def __init__(self, arm, p, PositiveReward = 1, NegativeReward = 0):
        self.p = p
        self.arm = arm
        self.PositiveReward = PositiveReward
        self.NegativeReward = NegativeReward

        

    def play(self,arm_id):
         reward = self.reward(arm_id)
         return reward
        

    def reward(self,arm_id):
        p = self.p[arm_id]
        random_num  = random.random()
        if random_num < p:
            return self.PositiveReward
        else:
            return self.NegativeReward
