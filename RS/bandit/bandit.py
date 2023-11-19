import random
class Bandit:
    
    def __init__(self,arm,p):
        self.p = p
        self.arm = arm
        

    def play(self,arm_id):
         reward = self.reward(arm_id)
         return reward
        

    def reward(self,arm_id):
        p = self.p[arm_id]
        random_num  = random.random()
        if random_num < p:
            return 1
        else:
            return 0

        
        

