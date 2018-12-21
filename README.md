# AURES_agentbased

With the AURES code, you can simulate auctions for renewable energy. Particularly, the simulation is for uniform pricing and pay-as-bid. For more details, please view the paper:

https://www.researchgate.net/publication/319956827_Putting_renewable_energy_auctions_into_action_-_An_agent-based_model_of_onshore_wind_power_auctions_in_Germany

Please also cite this paper when you use the code (Putting renewable energy auctions into action – An agent-based model of onshore wind power auctions in Germany; August 2017; Energy Policy 110(November 2017):pp. 394-402; DOI: 10.1016/j.enpol.2017.08.024)


Further instructions for using the code:

The AURES agentbased code uses the agentbased infrastructure mesa as a basis: https://github.com/projectmesa/mesa

To enable the code to run smoothly, a slight adaptation to the mesa framework has to be made:

At mesa time.py, a step for degression has to be included:

class RandomActivation(BaseScheduler):
    '''
    A scheduler which activates each agent once per step, in random order,
    with the order reshuffled every step.

    This is equivalent to the NetLogo 'ask agents...' and is generally the
    default behavior for an ABM.

    Assumes that all agents have a step(model) method.
    '''

    def step(self):
        '''
        Executes the step of all agents, one at a time, in random order.
        '''
        random.shuffle(self.agents)

        for agent in self.agents:
            agent.step(self.model)
        self.steps += 1
        self.time += 1

    def degression(self):
        '''
        Executes the degression of all agents, one at a time, in random order.
        '''
        random.shuffle(self.agents)

        for agent in self.agents:
            agent.degression(self.model)
