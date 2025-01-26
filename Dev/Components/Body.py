from Components.Attributes import Attributes
from Components.Genome import Genome

class Body:
    """
    Contains the current state attributes and genome of the 
    agent.
    """
    
    #==================================================[Initialization]==================================================
    def __init__(self, Attributes:Attributes, Genome:Genome):
        """
        Creates A body object
        
        Args:
            Attributes (Attributes): _description_
            Genome (Genome): _description_
        """
        
        self.attributes = Attributes
        self.genome = Genome
    
    #==================================================[Utility methods]==================================================
    def __repr__(self):
        return f"Body(Attributes={self.attributes},Genome={self.genome})"
    
    
        