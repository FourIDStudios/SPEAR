#Library Imports
import threading
from Components.Genome import Genome
from Components.Brain import Brain
from Components.Attributes import Attributes
from Components.Body import Body

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
        self.body = Body(Attributes(),Genome(parentGenome))
        self.brain = Brain(self.body)
        
        # Add a threading event for stopping the think process
        self._stop_event = threading.Event()

        # Start the think process in a separate thread
        self._think_thread = threading.Thread(target=self.think, daemon=True)
        self._think_thread.start()
    
    #==================================================[Core methods]==================================================
    def think(self):
        """
        Starts the agent's decision-making process
        """
        while not self._stop_event.is_set():
            self.brain.Think(None)
    
    def stop(self):
        """
        Stops the agent's thinking process gracefully (I hope).
        """
        self._stop_event.set()
        if self._think_thread.is_alive():
            self._think_thread.join()
        
    
    #==================================================[Magic methods]==================================================
    def __str__(self):
        return f"Agent: {self.name} Genome: {self.genome} Brain: {self.brain}"
    
    def __repr__(self):
        return f"Agent: {self.name} Genome: {self.genome} Brain: {self.brain}"
        
        
            

    