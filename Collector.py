'''
Created on 22.07.2016

@author: Vasili
'''
from collections import OrderedDict
import csv



class Collector():
    global results
    results={}
    global iteration
    iteration=0
    def __init__(self):
        pass
    
    def start(self,model):
        global iteration
        iteration+=1
        newkey = (iteration,model.round)
        if model.name=="PaB":
            results[newkey] = (model.meanbid, model.supply, model.p_lim, model.mean_bid_overall, model.highest_bid, model.project_developers, model.citizen_companies, model.financial_investors,model.avg_profit)
        else:
            results[newkey] = (model.uni_price, model.supply, model.p_lim, model.highest_bid, model.project_developers, model.citizen_companies, model.financial_investors,model.avg_profit)
        return OrderedDict(sorted(results.items()))
    
    def cont(self,model):
        newkey = (iteration,model.round)
        if model.name=="PaB":
            results[newkey] = (model.meanbid, model.supply, model.p_lim, model.mean_bid_overall, model.highest_bid, model.project_developers, model.citizen_companies, model.financial_investors,model.avg_profit)
        else:
            results[newkey] = (model.uni_price, model.supply, model.p_lim, model.highest_bid, model.project_developers, model.citizen_companies, model.financial_investors,model.avg_profit)
        return OrderedDict(sorted(results.items()))
    
    def save(self,model):
        with open(str(model.name)+'.csv', 'w') as f:
            w = csv.writer(f,delimiter=';')
            w.writerows(results.items())
    
        
    
    
    