'''
Created on 13.06.2016

@author: Vasili
'''
import Bid_Function
from mesa import Agent
import random

"""This sheet defines the properties and behaviour of the participating agents."""

class Dev_Agent(Agent):
    """ Project Developer """
    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        self.type = "Project Developer"
        #Generate project's cost in €/kWh and power quantity in MW
        self.cost = round(random.uniform(5.9,6.7),2)
        self.amount = random.randint(10,40)
        #Distinguish between different pricing rules
        if model.name == "PaB" and model.round==0:
            #Maximize utility function
            pab_bid = Bid_Function.bidshading(model.T,self.cost,self.cost,model.p_lim,model.comp,model.succ,0.95).bidding #self.cost,self.cost,model.p_lim,model.comp,model.succ
            self.bid = (self.amount , pab_bid, self.type)
        else:
            self.bid = (self.amount , round(self.cost,2), self.type)
    #Advance model by one more round
    def step(self, model):
            #Distinguish between pricing rules
            #If agent's project has been chosen, his costs are decreasing and new power quantity is drawn
        if model.name=="PaB":
            pab_bid = Bid_Function.bidshading(model.T,self.cost,model.mean_bid_overall,model.p_lim,model.comp,model.succ,0.95).bidding #self.cost,model.mean_bid_overall,model.p_lim,model.comp,model.succ
            self.bid = (self.amount, pab_bid, self.type)
        elif model.name=="Descending":
            iv_bid=0.5*self.cost+0.5*model.uni_price
            self.bid=(self.amount , iv_bid)
        else:
            self.bid= (self.amount,round(self.cost,2),self.type)
            
    def degression(self,model):
        if self.bid[1] <= model.highest_bid:
            self.cost*=random.uniform(0.985,1.00)
            self.amount = random.randint(10,40)

    

class Comm_Agent(Agent):
    """ Citizens' Energy Company"""
    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        self.type = "Citizen Company"
        #Generate certain cost in €/kWh and power in MW of project
        self.cost = round(random.uniform(5.9,6.7),2)
        self.amount = random.randint(3,18)
        #Distinguish between different pricing rules
        if model.name == "PaB" and model.round==0:
            pab_bid = Bid_Function.bidshading(model.T,self.cost,self.cost,model.p_lim,model.comp,model.succ,0.6).bidding
            self.bid = (self.amount , pab_bid, self.type)
        else:
            self.bid = (self.amount , round(self.cost,2), self.type)
        self.round_in=0


    def step(self, model):
        if self.bid[1]>0:
            if model.name=="PaB":
                #Maximize utility function; with learning algorithm
                #Without any learning; same distribution in believe about the other agents' costs
                #def bid_shade(x):
                    #return -(x-self.cost)*numpy.power(1-scipy.stats.uniform.cdf(x, loc=self.cost, scale=1),6)
                    pab_bid = Bid_Function.bidshading(model.T,self.cost,model.mean_bid_overall,model.p_lim,model.comp,model.succ,0.6).bidding
                    self.bid = (self.amount , pab_bid, self.type)
            elif model.name=="Descending":
                iv_bid=0.5*self.cost+0.5*model.uni_price
                self.bid=(self.amount , iv_bid, self.type)
                        
    def degression(self,model):
        if self.bid[1] <= model.highest_bid and self.bid[1]>0:
            self.bid= (0,0,self.type)
            self.round_in=model.round+random.randint(4,8)
        elif self.bid[1]==0 and self.round_in==model.round:
            self.cost *=random.uniform(0.985,1.00)
            self.amount = random.randint(3,18)         
            self.bid=(self.amount , round(self.cost,2), self.type)


class Fin_Agent(Agent):
    """ Financial Investor """
    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        self.type = "Financial Investor"
        #Generate certain cost in €/kWh and power in MW of project
        self.cost = random.uniform(5.9,6.7)
        self.amount = random.randint(15,40)
        #Distinguish between different pricing rules
        if model.name == "PaB" and model.round==0:
            #Maximize utility function
            pab_bid = Bid_Function.bidshading(model.T,self.cost,self.cost,model.p_lim,model.comp,model.succ,0.9).bidding
            self.bid = (self.amount , pab_bid, self.type)
        else:
            self.bid = (self.amount , round(self.cost,2), self.type)
    #When next round is initiated
    def step(self, model):
        if model.name=="PaB":
            pab_bid = Bid_Function.bidshading(model.T,self.cost,model.mean_bid_overall,model.p_lim,model.comp,model.succ,0.9).bidding
            self.bid = (self.amount , pab_bid, self.type)
        else:
            self.bid= (self.amount,round(self.cost,2),self.type)
    
    def degression(self,model):
    #If agent's project has been chosen, his costs are decreasing and a new project is developed
        if self.bid[1] <= model.highest_bid:
            self.cost*=random.uniform(0.985,1.00)
            self.amount = random.randint(15,40)

