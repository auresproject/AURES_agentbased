'''
Created on 04.06.2016

@author: Vasili
'''
from Models import Uniform

"""First line determines how many iterations the simulation will have.
Then model is run with the following parameters: 
number of project developers, citizens' energy companies, financial investors, 
demand per round in MW and price limit.
Range(T) defines how many auctions rounds will take place in each iteration."""

for i in range(1):
    model = Uniform(100,60,14,800,7)
    for i in range(13):
        model.step()
