#Library Imports

from Components.Genome import Genome
from Components.Brain import Brain

class Agent:
    """
    The agent class that holds the FSM and Genome of the agent
    """
    
    #==================================================[Initialization]==================================================
    def __init__(self, name, parentGenome=None):
        """
        Initializes the agent with a name, genome and brain
        """
        self.name = name
        self.genome = Genome(parentGenome)
        self.brain = Brain()
    
    #==================================================[Core methods]==================================================
    def think(self):
        """
        Starts the agent's decision-making process
        """
        self.brain.Think(None)
    
    
    #==================================================[Magic methods]==================================================
    def __str__(self):
        return f"Agent: {self.name} Genome: {self.genome} Brain: {self.brain}"
    
    def __repr__(self):
        return f"Agent: {self.name} Genome: {self.genome} Brain: {self.brain}"
        
        
            

    