# AURES_agentbased

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
