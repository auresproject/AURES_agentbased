'''
Created on 04.06.2016

@author: Vasili
'''
from Models import PaB


"""First line determines how many iterations the simulation will have.
Then model is run with the following parameters: 
number of project developers, citizens' energy companies, financial investors, 
demand per round in MW and price limit in ct/kWh and rounds per iteration without the initial one.
Range(T) defines how many auctions rounds will take place in each iteration and T has
to be the same as in the parameters above."""

for i in range(1):
    model = PaB(100,60,14,800,7)
    for i in range(13):
        model.step()
    
