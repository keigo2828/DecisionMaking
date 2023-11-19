from bandit import Bandit
from policy.RS import RS 
import pandas as pd
import os
#from datetime import datetime

class Sim:
    def __init__(self,sim,step,arm,level,p):
        self.policy = RS(arm,level,sim,step)
        self.bandit = Bandit(arm,p)
        self.sim = sim
        self.step = step
        self.p = p
        self.level = level
    
    def run(self):
        for sim_ct in range(self.sim):
            for step_ct in range(self.step):
                action = self.policy.select_action(step_ct)
                reward = self.bandit.play(action)
                self.policy.update(reward, sim_ct, step_ct)
            #print(self.policy.rs_value) 
            self.policy.reset()
        #print(self.policy.action_history)

        os.makedirs("log", exist_ok = True )

        df = pd.DataFrame(self.policy.action_history)
        df.to_csv("log/free_action_sequence_p({},{})aleph{}.csv".format(self.p[0],self.p[1],self.level))


class Sim_Last_Make_Decesiton(Sim):

    def __init__(self,sim,step,arm,level,p,ct1,ct2):
        super().__init__(sim,step,arm,level,p)
        self.ct1 = ct1
        self.ct2 = ct2

    def run(self):
        for sim_ct in range(self.sim):

            for ct1  in range(self.ct1):
                action = 0
                reward = self.bandit.play(action)
                self.policy.choice_update(reward, sim_ct, ct1,action)
            for ct2 in range(self.ct2):
                action = 1
                reward = self.bandit.play(action)
                self.policy.choice_update(reward, sim_ct, (ct1 + ct2+1),action)
            action = self.policy.select_action(ct1 + ct2 + 2)
            reward = self.bandit.play(action)
            self.policy.update(reward, sim_ct, ct1 + ct2 + 2)
            print(self.policy.rs_value) 
            self.policy.reset()


        #print(self.policy.action_history)

        os.makedirs("log", exist_ok = True )

        df = pd.DataFrame(self.policy.action_history)
        df.to_csv("log/action_sequence_p({},{})aleph{}.csv".format(self.p[0],self.p[1],self.level))


        
        

def main():
    arm = 2
    sim = 10
    #step = 111

    level = 0.5
    p = [0.8,0.8]
    ct1 = 10
    ct2 = 10
    #sim = Sim(sim,step,arm,level,p)
    step = ct1 + ct2 + 1
    sim = Sim_Last_Make_Decesiton(sim,step,arm,level,p,ct1,ct2)
    sim.run()

if __name__ == '__main__':
    print('started run')
    main()
    print('finished run')
