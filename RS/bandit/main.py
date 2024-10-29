from bandit import Bandit
from policy.RS import RS 
from policy.RescorlaWagner import RescorlaWagner
import pandas as pd
import os
import optuna 
import numpy as np
import plotly.io as pio
#from datetime import datetime

class Sim:
    def __init__(self,sim,step,arm,level,p,alpha):
        self.policy = RS(arm,level,sim,step,alpha)
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
                self.policy.update_larning_rate(reward, sim_ct, step_ct)
            print(self.policy.rs_value) 
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
            #print(self.policy.rs_value) 
            self.policy.reset()

        os.makedirs("log", exist_ok = True )

        df = pd.DataFrame(self.policy.action_history)
        df.to_csv("log/action_sequence_p({},{})aleph{}.csv".format(self.p[0],self.p[1],self.level))




class Sim_tune(Sim):

    def __init__(self ,sim ,step ,arm ,level ,p ,ct1 ,ct2 ,alpha):
        super().__init__(sim,step,arm,level,p,alpha)
        self.ct1 = ct1
        self.ct2 = ct2


    def run(self):

        cwd = os.getcwd()
        tmp = 'data/outputcsv_01.csv'
        path = os.path.join(cwd,tmp)
        df = pd.read_csv(path)
        #実際に選択した行動
        Choice = df['Choice']
        #行動した選択を記録する配列
        CorrectActionList = []
        Order = df['Order']
        Slot = df['Slot']
        Slot_Result = df['Slot_Result']
        P = df['P']
        Uid = df['User_id']
        ct = 0
        ctwin = 0
        ctlose = 0

        for i in range(len(df)):
            if (True):
                #確率が大きくなったら保存するデータを変える
                pass

            action = Slot[i]
            #print(action)
            if Slot_Result[i] == 'Lose':
                reward = -1
                ctlose+= 1
            else:
                reward = 1
                ctwin+= 1

            #さん術平均
            self.policy.choice_update(reward, ct, Order[i], action)
            #学習りつ
            #self.policy.choice_update_larning_rate(reward, ct, Order[i], action)
            #print(self.policy.rs_value,self.policy.expected_value)  
            if Order[i] == 31:
                print(self.policy.expected_value,self.policy.rs_value,self.policy.bandit_ct/np.sum(self.policy.bandit_ct)) 
                action = self.policy.select_action(32)
                CorrectActionList.append(Choice[i])
                #print(CorrectActionList)
                reward = self.bandit.play(action)
                self.policy.update(reward, ct, 32)
                #self.policy.update_larning_rate(reward, ct, 32)
                #print(self.policy.expected_value,self.policy.rs_value) 
                self.policy.reset()
                ct += 1

        #print(self.policy.action_history)

        #os.makedirs("log", exist_ok = True )

        #行の出力にはここを変更

        df = pd.DataFrame(self.policy.action_history)
        #df1 = pd.DataFrame(CorrectActionList)
       

       #最終行を取得
        SimuActionList = self.policy.action_history[:,32]
       
    

        #print(len(SimuActionList),sum(SimuActionList-CorrectActionList),sum((SimuActionList-CorrectActionList)**2),1- sum((SimuActionList-CorrectActionList)**2/len(SimuActionList)))
        #df2 = pd.DataFrame(SimuActionList)

        #正答率を取得

        #Correctrate = 1 - sum((SimuActionList-CorrectActionList)**2/len(SimuActionList))
        #return Correctrate
    
        #最小事情誤差
        # taskLength = len(SimuActionList)/9
        # splitsim  = np.array_split(SimuActionList, 9)
        # splitcorr = np.array_split(CorrectActionList, 9)
        # y = 0
        # for i in range(9):
        #     y += (sum(splitsim[i])/taskLength - sum(splitcorr[i])/taskLength)**2
        # return y

        
        

    
        #nparrayにして
        #片方の配列から片方を引いて二乗する
        #1 - sum(list)/len(list)  正答率　間違っている時は配列に1が入っている

        #行の出力にはここを変更
        df.to_csv("log/test1_csv_action_sequence_p({},{})aleph{}.csv".format(self.p[0],self.p[1],self.level))
        df.to_csv("RS_bayse_best_count_mean_300.csv")
        # df1.to_csv("log/correct.csv")
        # df2.to_csv("log/sim.csv")


class InSim_tune(Sim):

    def __init__(self ,sim ,step ,arm ,level ,p ,ct1 ,ct2 ,alpha,id):
        super().__init__(sim,step,arm,level,p,alpha)
        self.ct1 = ct1
        self.ct2 = ct2
        self.uid = id 

    def run(self):
        cwd = os.getcwd()
        tmp = 'data/outputcsv_01.csv'
        path = os.path.join(cwd,tmp)
        df = pd.read_csv(path)
        df = df[df.User_id == self.uid]
        #実際に選択した行動
        Choice = df['Choice']
        #行動した選択を記録する配列
        CorrectActionList = []
        Order = df['Order']
        Slot = df['Slot']
        Slot_Result = df['Slot_Result']
        P = df['P']
        Uid = df['User_id']
        ct = 0
        ctwin = 0
        ctlose = 0
        

        for i in range(len(df)):
            action = Slot.iloc[i]
            #print(action)
            if Slot_Result.iloc[i] == 'Lose':
                reward = -1
                ctlose+= 1
            else:
                reward = 1
                ctwin+= 1

            #さん術平均
            self.policy.choice_update(reward, ct, Order.iloc[i], action)

            if Order.iloc[i] == 31:
                # print(self.policy.expected_value,self.policy.rs_value) 
                action = self.policy.select_action(32)
                CorrectActionList.append(Choice.iloc[i])
                reward = self.bandit.play(action)
                self.policy.update(reward, ct, 32)
                #self.policy.update_larning_rate(reward, ct, 32)
                self.policy.reset()
                ct += 1

        #行の出力にはここを変更
        df = pd.DataFrame(self.policy.action_history)
        #df1 = pd.DataFrame(CorrectActionList)
       #最終行を取得
        SimuActionList = self.policy.action_history[:,32]
        # print(SimuActionList[8])
        # print(CorrectActionList)
        # quit()

        #df2 = pd.DataFrame(SimuActionList)

        #最小事情誤差
        y = 0
        for i in range(9):
            y += (SimuActionList[i] - CorrectActionList[i])**2
        return y
    

        #nparrayにして
        #片方の配列から片方を引いて二乗する
        #1 - sum(list)/len(list)  正答率　間違っている時は配列に1が入っている
        #行の出力にはここを変更
        df.to_csv("log/test1_csv_action_sequence_p({},{})aleph{}.csv".format(self.p[0],self.p[1],self.level))
        df.to_csv("RS_bayse_best_count_mean_300.csv")
        # df1.to_csv("log/correct.csv")
        # df2.to_csv("log/sim.csv")


class Sim_tune_RW(Sim):

    def __init__(self ,sim ,step ,arm ,p ,ct1 ,ct2 ,alpha ,beta):
        self.policy_RW = RescorlaWagner(arm,sim,step,alpha,beta)
        self.bandit = Bandit(arm,p)
        self.sim = sim
        self.step = step
        self.p = p
        self.ct1 = ct1
        self.ct2 = ct2


    def run(self):

        cwd = os.getcwd()
        tmp = 'data/outputcsv_01.csv'
        path = os.path.join(cwd,tmp)
        df = pd.read_csv(path)
        #実際に選択した行動
        Choice = df['Choice']
        #行動した選択を記録する配列
        CorrectActionList = []
        Order = df['Order']
        Slot = df['Slot']
        Slot_Result = df['Slot_Result']
        P = df['P']
        Uid = df['User_id']
        ct = 0


        for i in range(len(df)):
            if (True):
                #確率が大きくなったら保存するデータを変える
                pass



            action = Slot[i]
            #print(action)
            if Slot_Result[i] == 'Lose':
                reward = -1
            else:
                reward = 1
            #self.policy.choice_update(reward, ct, Order[i], action)
            self.policy_RW.choice_update_larning_rate(reward, ct, Order[i], action)

            if Order[i] == 31:
                
                action = self.policy_RW.select_action(32)
                CorrectActionList.append(Choice[i])
                #print(action)
                reward = self.bandit.play(action)

                #self.policy.update(reward, ct, 32)
                self.policy_RW.update_larning_rate(reward, ct, 32)

                #print(self.policy.expected_value,self.policy.rs_value) 
                self.policy_RW.reset()
                ct += 1



        #print(self.policy.action_history)

        #os.makedirs("log", exist_ok = True )

        #行の出力にはここを変更

        df = pd.DataFrame(self.policy_RW.action_history)
       # df1 = pd.DataFrame(CorrectActionList)
       

       #最終行を取得
        SimuActionList = self.policy_RW.action_history[:,32]

        #print(len(SimuActionList),sum(SimuActionList-CorrectActionList),sum((SimuActionList-CorrectActionList)**2),1- sum((SimuActionList-CorrectActionList)**2/len(SimuActionList)))
        #df2 = pd.DataFrame(SimuActionList)

        #正答率を取得

        #Correctrate = 1 - sum((SimuActionList-CorrectActionList)**2/len(SimuActionList))
        #return Correctrate
    

        #最小事情誤差
        # taskLength = len(SimuActionList)/9
        # splitsim  = np.array_split(SimuActionList, 9)
        # splitcorr = np.array_split(CorrectActionList, 9)
        # y = 0
        # for i in range(9):
        #     y += (sum(splitsim[i])/taskLength - sum(splitcorr[i])/taskLength)**2
        # return y

        
        

    
        #nparrayにして
        #片方の配列から片方を引いて二乗する
        #1 - sum(list)/len(list)  正答率　間違っている時は配列に1が入っている

        #行の出力にはここを変更
        #df.to_csv("log/test1_csv_action_sequence_p({},{})aleph{}.csv".format(self.p[0],self.p[1],self.level))
        df.to_csv("rwbest_softmax_300_700_new.csv")
        # df1.to_csv("log/correct.csv")
        # df2.to_csv("log/sim.csv")



class Sim_CSV(Sim):

    def __init__(self,sim,step,arm,level,p,ct1,ct2,):
        super().__init__(sim,step,arm,level,p)
        self.ct1 = ct1
        self.ct2 = ct2


    def run(self):

        cwd = os.getcwd()
        tmp = 'data/outputcsv_01.csv'
        path = os.path.join(cwd,tmp)
        df = pd.read_csv(path)
        #Choice = df['Choice']
        Order = df['Order']
        Slot = df['Slot']
        Slot_Result = df['Slot_Result']
        P = df['P']
        Uid = df['User_id']
        ct = 0


        for i in range(len(df)):
            if (True):
                #確率が大きくなったら保存するデータを変える
                pass



            action = Slot[i]
            #print(action)
            if Slot_Result[i] == 'Lose':
                reward = -1
            else:
                reward = 1
            #self.policy.choice_update(reward, ct, Order[i], action)
            self.policy.choice_update_larning_rate(reward, ct, Order[i], action)

            if Order[i] == 32:
                action = self.policy.select_action(32)
                print(action)
                reward = self.bandit.play(action)

                #self.policy.update(reward, ct, 32)
                self.policy.update_larning_rate(reward, ct, 32)

                print(self.policy.expected_value,self.policy.rs_value) 
                self.policy.reset()
                ct += 1



        #print(self.policy.action_history)

        os.makedirs("log", exist_ok = True )

        df = pd.DataFrame(self.policy.action_history)
        df.to_csv("log/test1_csv_action_sequence_p({},{})aleph{}.csv".format(self.p[0],self.p[1],self.level))




def main(Alpha,Level):
    arm = 2
    sim = 244*9
    #step = 111

    level = Level
    alpha = Alpha
    p = [0.9,0.9]
    ct1 = 8
    ct2 = 24
    step = 33
    #sim = Sim(sim,step,arm,level,p)
    #sim = Sim_CSV(sim,step,arm,level,p,ct1,ct2)
    sim = Sim_tune(sim,step,arm,level,p,ct1,ct2,alpha)
    CorrectRate = sim.run()
    return CorrectRate

def Inmain(Alpha,Level,id):
    arm = 2
    sim = 9
    level = Level
    alpha = Alpha
    p = [0.9,0.9]
    ct1 = 8
    ct2 = 24
    step = 33
    sim = InSim_tune(sim,step,arm,level,p,ct1,ct2,alpha,id)
    CorrectRate = sim.run()
    return CorrectRate

def main_RW(Alpha,Beta):
    arm = 2
    sim = 244*9
    #step = 111

    beta = Beta
    alpha = Alpha
    p = [0.9,0.9]
    ct1 = 8
    ct2 = 24
    step = 33
    #sim = Sim(sim,step,arm,level,p)
    #sim = Sim_CSV(sim,step,arm,level,p,ct1,ct2)

    sim = Sim_tune_RW(sim,step,arm,p,ct1,ct2,alpha,beta)
    CorrectRate = sim.run()
    return CorrectRate


    #目的関数
def objective(trial):

    Alpha = trial.suggest_float("Alpha", 0.1, 0.2)
    Level = trial.suggest_float("Level", 0.3, 0.7)

    CorrectRate = main(Alpha,Level)
    
    return CorrectRate

def objective_mean(trial):

    #Alpha = trial.suggest_float("Alpha", 0.1, 0.2)
    Level = trial.suggest_float("Aspiration_Level", -1, 1)

    CorrectRate = main(0,Level)
    
    return CorrectRate

def objective_RW(trial):

    Alpha = trial.suggest_float("Alpha", 0, 1)
    Beta = trial.suggest_float("Beta", 0, 700)

    CorrectRate = main_RW(Alpha,Beta)
    
    return CorrectRate

def INobjective_mean(id):

    def inobjective_mean(trial):
        Level = trial.suggest_float("Aspiration_Level", -1, 1)
        CorrectRate = Inmain(0,Level,id)
        return CorrectRate
    
    return inobjective_mean

def IndividualParametersEST(ID):
    for id in range(ID):
        study = optuna.create_study(study_name="my_study:{}".format(id), storage="sqlite:///example.db" , direction="minimize")
        study.optimize(INobjective_mean(id), n_trials=300)
        trial = study.best_trial
        print("Accuracy: {}".format(trial.value))
        print("Best hyperparameters: {}".format(trial.params))


if __name__ == '__main__':
    print('started run')

    #main(0,-0.2500)
    main(0,-0.25)
    #main_RW( 0.01377, 339.7)

    # IndividualParametersEST(244)

    #目的関数を最小化
    # study = optuna.create_study(direction="minimize")

    # # study.optimize(objective_RW, n_trials=300)
    # study.optimize(INobjective_mean, n_trials=300)
    # # #study.optimize(objective, n_trials=300)

    # trial = study.best_trial

    # print("Accuracy: {}".format(trial.value))
    # print("Best hyperparameters: {}".format(trial.params))
    # slice_fig = optuna.visualization.plot_slice(study)
    # # contour_fig  = optuna.visualization.plot_contour(study, params=["Alpha","Beta"])
    # #contour_fig  = optuna.visualization.plot_contour(study, params=["Aspiration_Level"])
    # #slice_fig.write_image("slice_plot_RW_softmax_1000_300.png")
    # slice_fig.write_image("slice__plot_RS_-11_300.png")
    # #contour_fig.write_image("contour_plot_RS_01_50.png")

    print('finished run')
