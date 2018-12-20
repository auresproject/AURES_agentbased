'''
Created on 14.07.2016

@author: Vasili
'''
import scipy.optimize
import scipy.stats
import scipy.special
import numpy


class bidshading:
    def __init__(self,T,c,mü,p_lim,comp,succ,discount):
        def bid(x,T,c,mü,comp,succ,discount):
            summe = 0
            for t in T:
                adding = - discount**t*(x[t]-c)
                prob=0
                for i in range(succ):
                    prob+=(scipy.special.binom(comp-1,i)*scipy.stats.norm.cdf(x[t], loc=mü, scale=0.3)**i*(1-scipy.stats.norm.cdf(x[t], loc=mü, scale=0.3))**(comp-1-i))
                if t == 0:
                    adding*=prob
                    summe+=adding
                else:
                    adding*=prob
                    prob_lose=0
                    for h in range(t):
                        prob_lose=0
                        for i in range(succ,comp):
                            prob_lose+=(scipy.special.binom(comp-1,i)*scipy.stats.norm.cdf(x[t-h-1], loc=mü, scale=0.3)**i*(1-scipy.stats.norm.cdf(x[t-h-1], loc=mü, scale=0.3))**(comp-1-i))
                        adding*=prob_lose
                    summe += adding
            return summe
        
        #comp,succ
        #**(comp-succ+1)))
        x0=numpy.array([c]*len(T))
        cons = ({'type': 'ineq', 'fun': lambda x:  p_lim-x[:]},{'type': 'ineq', 'fun': lambda x:  x[:]-c-0.01})
        #res=scipy.optimize.differential_evolution(bid,bounds=[(c,p_lim)]*len(T),args=(T,c,mü,comp,succ,discount))
        #res=scipy.optimize.brute(bid,ranges=[(c,p_lim)]*len(T),args=(T,c,mü,comp,succ,discount),Ns=10,finish=None)
        res=scipy.optimize.minimize(bid,x0,args=(T,c,mü,comp,succ,discount),method='SLSQP',constraints=cons)        
        self.bidding = round(res.x.item(0),2)        

