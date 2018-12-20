'''
Created on 04.06.2016

@author: Vasili
'''

from mesa import Model
from mesa.time import RandomActivation
import Agents
import random
from Collector import Collector
import matplotlib.pyplot as plt


class PaB(Model):
    """A Pay as Bid Auction."""
    def __init__(self, P, C, F, d, p_lim):
        print("geht los")
        self.name = "PaB"
        self.running = True
        self.num_f_agents = F
        self.num_c_agents = C
        self.num_d_agents = P
        self.schedule = RandomActivation(self)        
        self.demand = d
        self.p_lim = p_lim
        self.round = 0
        self.T=list(range(4))
        # Create agents
        self.comp=150
        self.ini_comp=150
        self.succ=50
        for i in range(self.num_f_agents):
            a = Agents.Fin_Agent(i, self)
            self.schedule.add(a)
        for i in range(self.num_c_agents):
            c = Agents.Comm_Agent(i, self)
            self.schedule.add(c)
        for i in range(self.num_d_agents):
            p = Agents.Dev_Agent(i, self)
            self.schedule.add(p)
    
        
        # Sort bids
        agent_bids = [a.bid for a in self.schedule.agents if a.bid[1]<=self.p_lim and a.bid[1]>0]
        blocked=len(self.schedule.agents)-len(agent_bids)
        s_agent_bids=sorted(agent_bids, key=lambda bid: (bid[1],bid[0]))
        supply=0
        agg=0
        self.succ=0
        
        # Algorithm to choose the winning bids
        for bid in s_agent_bids:
            if supply < self.demand:
                supply+=bid[0]
                agg+=bid[0]*bid[1]
                self.uni_price=bid[1]
                self.highest_bid=bid[1]
                self.succ+=1
                self.agg_bids=agg
                self.supply_bids=supply
            elif bid[1]<self.p_lim:
                self.agg_bids+=(bid[0]*bid[1])
                self.supply_bids+=bid[0]
        self.project_developers=0
        self.citizen_companies=0
        self.financial_investors=0
        self.winner=0
        self.surplus=0
        for a in self.schedule.agents:
            if a.bid[1] <= self.highest_bid and a.bid[1]>0:
                self.winner+=1
                self.surplus+=((a.bid[1]-a.cost)*a.bid[0])
                if a.bid[2]=="Project Developer":
                    self.project_developers+=1
                elif a.bid[2]=="Citizen Company":
                    self.citizen_companies+=1
                else:
                    self.financial_investors+=1
        self.avg_profit=self.surplus/supply
        self.comp=len(s_agent_bids)
        self.ini_comp=len(agent_bids)        
        # Calculation of mean winning bid
        self.highest_bids=[]
        self.highest_bids.append(self.highest_bid)
        print(agg)
        print(supply)
        print(self.agg_bids)
        print(self.supply_bids)
        self.meanbid=round(agg/supply,2)
        
        # Calculation of mean overall bid
        self.mean_bid_overall=round(self.agg_bids/self.supply_bids,2)
        print("overall mean bid: "+str(self.mean_bid_overall)+"and highest bid: "+str(self.highest_bid))
        print("Menge: "+str(supply)+"MW zu Durchschnittspreis: "+str(self.meanbid)+" ct/kWh mit "+str(blocked)+" abgelehnten Geboten!")

        x_ax=[0]
        x=0
        y_ax=[]
        width=[]
        # Create the graphs
        for i in range(len(s_agent_bids)-1):
            x+=s_agent_bids[i][0]
            x_ax.append(x)
            width.append(s_agent_bids[i][0])
            y_ax.append(s_agent_bids[i][1])
        print(x_ax)
        print(y_ax)

        #x_ax.pop()
        #plt.bar(x_ax, y_ax, width=width, align="edge")
        #plt.plot([supply, supply], [0, 7], 'r-', lw=4)
        #plt.savefig('/Users/Vasili/Desktop/Masterarbeit/Grafiken/PaB/PaB_'+str(self.round)+'.png')
        plt.clf()
        #plt.show()
        self.supply=supply
        print(Collector.start(0,self))
        self.schedule.degression()


    def step(self):
        """Advance the model by one step."""
        # Create new agents participating in this round
        self.T.pop()
        self.round+=1
        if len(self.T)==0:
            if self.round==12:
                self.T=list(range(2))
            else:
                self.T=list(range(4))
        for i in range(random.randint(0,2)):
            a = Agents.Fin_Agent(i, self)
            self.schedule.add(a)
        for i in range(random.randint(6,12)):
            c = Agents.Comm_Agent(i, self)
            self.schedule.add(c)
        for i in range(random.randint(0,2)):
            p = Agents.Dev_Agent(i, self)
            self.schedule.add(p)
        if self.round>2:
            self.p_lim=round((self.highest_bids[-1]+self.highest_bids[-2]+self.highest_bids[-3])/3*1.08,2)
        self.schedule.step()
        agent_bids = [a.bid for a in self.schedule.agents if a.bid[1]<=self.p_lim and a.bid[1]>0]
        blocked=len(self.schedule.agents)-len(agent_bids)
        s_agent_bids=sorted(agent_bids, key=lambda bid: (bid[1],bid[0]))
        supply=0
        agg=0
        self.succ=0
        for bid in s_agent_bids:
            if supply < self.demand:
                supply+=bid[0]
                agg+=bid[0]*bid[1]
                self.uni_price=bid[1]
                self.highest_bid=bid[1]
                self.succ+=1
                self.agg_bids=agg
                self.supply_bids=supply
            elif bid[1]<self.p_lim:
                self.agg_bids+=(bid[0]*bid[1])
                self.supply_bids+=bid[0]
        
        self.project_developers=0
        self.citizen_companies=0
        self.financial_investors=0
        
        self.winner=0
        self.surplus=0
        for a in self.schedule.agents:
            if a.bid[1] < self.highest_bid and a.bid[1]>0:
                print(a.bid[1]-a.cost)
                self.winner+=1
                self.surplus+=((a.bid[1]-a.cost)*a.bid[0])
                self.winner+=1
                if a.bid[2]=="Project Developer":
                    self.project_developers+=1
                elif a.bid[2]=="Citizen Company":
                    self.citizen_companies+=1
                else:
                    self.financial_investors+=1
        self.avg_profit=self.surplus/supply        
        
        self.comp=len(s_agent_bids)
        self.highest_bids.append(self.highest_bid)
        self.meanbid=round(agg/supply,2)
        
        # Calculation of mean overall bid
        self.mean_bid_overall=round(self.agg_bids/self.supply_bids,2)
        print("overall mean bid: "+str(self.mean_bid_overall)+" and highest bid: "+str(self.highest_bid))
        print("Menge: "+str(supply)+"MW zu Durchschnittspreis: "+str(self.meanbid)+" ct/kWh mit "+str(blocked)+" abgelehnten Geboten und "+str(self.winner)+" Sieger!")

        x_ax=[0]
        x=0
        y_ax=[]
        width=[]
        for i in range(len(s_agent_bids)-1):
            x+=s_agent_bids[i][0]
            x_ax.append(x)
            width.append(s_agent_bids[i][0])
            y_ax.append(s_agent_bids[i][1])
        #x_ax.pop()
        #plt.bar(x_ax, y_ax, width=width, align="edge")
        print(x_ax)
        print(y_ax)
        #plt.plot([supply, supply], [0, 7], 'r-', lw=4)
        #plt.savefig('/Users/Vasili/Desktop/Masterarbeit/Grafiken/PaB/PaB_'+str(self.round)+'.png')
        #plt.clf()
        #plt.show()
        self.supply=supply
        print(Collector.cont(0,self))
        Collector.save(0, self)
        self.schedule.degression()




class Uniform(Model):
    """An Uniform Pricing Auction Model."""
    def __init__(self, P, C, F, d, p_lim):
        self.name = "Uniform"
        self.running = True
        self.num_f_agents = F
        self.num_c_agents = C
        self.num_d_agents = P
        self.schedule = RandomActivation(self)
        self.p_lim=p_lim
        
        self.demand = d
        self.round = 0
        # Create agents
        for i in range(self.num_f_agents):
            a = Agents.Fin_Agent(i, self)
            self.schedule.add(a)
        for i in range(self.num_c_agents):
            c = Agents.Comm_Agent(i, self)
            self.schedule.add(c)
        for i in range(self.num_c_agents):
            p = Agents.Dev_Agent(i, self)
            self.schedule.add(p)
        
        agent_bids = [a.bid for a in self.schedule.agents if a.bid[1]<=self.p_lim and a.bid[1]>0]
        s_agent_bids=sorted(agent_bids, key=lambda price: price[1])
        supply=0
        agg=0
        for bid in s_agent_bids:
            if supply < self.demand:
                supply+=bid[0]
                agg+=bid[0]*bid[1]
                self.uni_price=bid[1]
                self.highest_bid=bid[1]
            else:
                #lowest rejected bid
                self.uni_price=bid[1]
                break
        self.highest_bids=[]
        self.highest_bids.append(self.highest_bid)
        
        self.project_developers=0
        self.citizen_companies=0
        self.financial_investors=0
        self.winner=0
        self.surplus=0
        for a in self.schedule.agents:
            if a.bid[1] < self.uni_price and a.bid[1]>0:
                self.winner+=1
                self.surplus+=((self.uni_price-a.cost)*a.bid[0])
                if a.bid[2]=="Project Developer":
                    self.project_developers+=1
                elif a.bid[2]=="Citizen Company":
                    self.citizen_companies+=1
                else:
                    self.financial_investors+=1
        
        self.avg_profit=self.surplus/supply
        #Plotting of the order
        x_ax=[0]
        x=0
        y_ax=[]
        width=[]
        for i in range(len(s_agent_bids)-1):
            x+=s_agent_bids[i][0]
            x_ax.append(x)
            width.append(s_agent_bids[i][0])
            y_ax.append(s_agent_bids[i][1])
        #x_ax.pop()
        print(x_ax)
        print(y_ax)

        #print(x_ax)
        #print(y_ax)
        print("Menge: "+str(supply)+"MW zu Preis: "+str(self.uni_price)+", "+str(self.winner)+" Gewinnern und "+str(self.highest_bid)+" höchstem bezuschlagten Gebot!")
        #plt.bar(x_ax, y_ax, width=width, align="edge")
        #plt.plot([supply, supply], [0, self.highest_bid], 'r-', lw=2)

        #plt.savefig('/Users/Vasili/Desktop/Masterarbeit/Grafiken/Uniform/Uniform.png', format='png')
        #plt.clf()
        #plt.show()
        self.supply=supply
        print(Collector.start(0,self))
        
        #Cost degression for the agents' costs
        self.schedule.degression()


    def step(self):
        '''Advance the model by one step.'''
        for i in range(random.randint(0,2)):
            a = Agents.Fin_Agent(i, self)
            self.schedule.add(a)
        for i in range(random.randint(6,12)):
            c = Agents.Comm_Agent(i, self)
            self.schedule.add(c)
        for i in range(random.randint(0,2)):
            p = Agents.Dev_Agent(i, self)
            self.schedule.add(p)
        self.round+=1
        if self.round>2:
            self.p_lim=round((self.highest_bids[-1]+self.highest_bids[-2]+self.highest_bids[-3])/3*1.08,2)
        self.schedule.step()
        agent_bids = [a.bid for a in self.schedule.agents if a.bid[1]<=self.p_lim and a.bid[1]>0]
        s_agent_bids=sorted(agent_bids, key=lambda price: price[1])
        supply=0
        agg=0
        for bid in s_agent_bids:
            if supply < self.demand:
                supply+=bid[0]
                agg+=bid[0]*bid[1]
                self.uni_price=bid[1]
                self.highest_bid=bid[1]
            else:
                #lowest rejected bid
                self.uni_price=bid[1]
                break
        self.highest_bids.append(self.highest_bid)
        
        #Counting type of winning agents
        self.project_developers=0
        self.citizen_companies=0
        self.financial_investors=0
        self.winner=0
        self.surplus=0
        for a in self.schedule.agents:
            if a.bid[1] < self.uni_price and a.bid[1]>0:
                self.winner+=1
                self.surplus+=((self.uni_price-a.cost)*a.bid[0])
                if a.bid[2]=="Project Developer":
                    self.project_developers+=1
                elif a.bid[2]=="Citizen Company":
                    self.citizen_companies+=1
                else:
                    self.financial_investors+=1
        self.avg_profit=self.surplus/supply

        x_ax=[0]
        x=0
        y_ax=[]
        width=[]
        for i in range(len(s_agent_bids)-1):
            x+=s_agent_bids[i][0]
            x_ax.append(x)
            width.append(s_agent_bids[i][0])
            y_ax.append(s_agent_bids[i][1])
        #x_ax.pop()
        print(x_ax)
        print(y_ax)

        print("Menge: "+str(supply)+"MW zu Preis: "+str(self.uni_price)+", "+str(self.winner)+" Gewinnern und "+str(self.highest_bid)+" höchstem bezuschlagten Gebot!")
        #plt.bar(x_ax, y_ax, width=width, align="edge")
        #plt.plot([supply, supply], [0, self.highest_bid], 'r-', lw=2)
        #plt.savefig('/Users/Vasili/Desktop/Masterarbeit/Grafiken/Uniform/Uniform_'+str(self.round)+'.png', format='png')
        #plt.clf()
        #plt.show()

        self.supply=supply
        print(Collector.cont(0,self))
        Collector.save(0, self)
        self.schedule.degression()


class Descending(Model):
    """A Descending Clock Auction Model."""
    def __init__(self, F, C, P, d, p_start, inc):
        self.name = "Descending"
        self.running = True
        self.num_f_agents = F
        self.num_c_agents = C
        self.num_d_agents = P
        self.schedule = RandomActivation(self)
        self.inc=inc
        self.p_start=p_start
        
        self.demand = d
        self.round = 1
        # Create agents
        for i in range(self.num_f_agents):
            a = Agents.Fin_Agent(i, self)
            self.schedule.add(a)
        for i in range(self.num_c_agents):
            c = Agents.Comm_Agent(i, self)
            self.schedule.add(c)
        for i in range(self.num_c_agents):
            p = Agents.Fin_Agent(i, self)
            self.schedule.add(p)
        
        agent_bids = [a.bid for a in self.schedule.agents if a.bid[1]>0]
        blocked=len(self.schedule.agents)-len(agent_bids)
        s_agent_bids=sorted(agent_bids, key=lambda price: price[1])
        supply=0
        for bid in s_agent_bids:
            if bid[1]<=self.p_start:
                supply+=bid[0]
        self.uni_price=self.p_start
        self.p=self.p_start
        while supply>800:
            self.p-=self.inc
            print(self.p)
            supply=0
            for bid in s_agent_bids:
                if bid[1]<=self.p:
                    supply+=bid[0]
        else:
            self.supply=supply
            self.uni_price=round(self.p,2)            
            print("Menge: "+str(supply)+"MW zu Preis: "+str(self.uni_price)+" ct/kWh mit "+str(blocked)+" abgelehnten Geboten!")
            
        x_ax=[0]
        x=0
        y_ax=[]
        width=[]
        for i in range(len(s_agent_bids)-1):
            x+=s_agent_bids[i][0]
            x_ax.append(x)
            width.append(s_agent_bids[i][0])
            y_ax.append(s_agent_bids[i][1])
        x_ax.pop()

        
        plt.bar(x_ax, y_ax, width=width, align="edge")
        plt.plot([supply, supply], [0, 7], 'r-', lw=4)
        plt.show()
        print(Collector.start(0,self))
        

    def step(self):
        '''Advance the model by one step.'''
        for i in range(random.randint(3,6)):
            a = Agents.Fin_Agent(i, self)
            self.schedule.add(a)
        for i in range(random.randint(3,6)):
            c = Agents.Comm_Agent(i, self)
            self.schedule.add(c)
        for i in range(random.randint(3,6)):
            p = Agents.Fin_Agent(i, self)
            self.schedule.add(p)
        self.schedule.step()
        self.round+=1
        agent_bids = [a.bid for a in self.schedule.agents if a.bid[1]>0]
        blocked=len(self.schedule.agents)-len(agent_bids)
        s_agent_bids=sorted(agent_bids, key=lambda price: price[1])
        supply=0
        for bid in s_agent_bids:
            if bid[1]<=self.p_start:
                supply+=bid[0]
        self.uni_price=self.p_start
        self.p=self.p_start
        while supply>800:
            self.p-=self.inc
            print(self.p)
            supply=0
            for bid in s_agent_bids:
                if bid[1]<=self.p:
                    supply+=bid[0]
        else:
            self.uni_price=round(self.p,2)
            self.supply=supply            
            print("Menge: "+str(supply)+"MW zu Preis: "+str(self.uni_price)+" ct/kWh mit "+str(blocked)+" abgelehnten Geboten!")
            
        x_ax=[0]
        x=0
        y_ax=[]
        width=[]
        for i in range(len(s_agent_bids)-1):
            x+=s_agent_bids[i][0]
            x_ax.append(x)
            width.append(s_agent_bids[i][0])
            y_ax.append(s_agent_bids[i][1])
        x_ax.pop()

        
        plt.bar(x_ax, y_ax, width=width, align="edge")
        plt.plot([supply, supply], [0, 7], 'r-', lw=4)
        plt.show()
        print(Collector.cont(0,self))