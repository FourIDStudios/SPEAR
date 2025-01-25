import time
import os
import json
import math

class Attribute:
    """
    Represents a single attribute of an agent.
    """
    def __init__(self, name, description, initial_value, min_value=None, max_value=None, optimal_value=None):
        """
        Initializes the attribute.
        """
        self.name = name
        self.description = description
        self.value = initial_value
        self.min_value = min_value
        self.max_value = max_value
        self.optimal_value = optimal_value
        pass
    
class Attributes:
    """
    Acts as a ‘whole’ representation of the agent's current state in a viewable form. 
    Represents the agent's current state, which fluctuates based on actions, environment, and time. 
    These attributes influence the agent's decision-making, behavior, and ability to perform tasks effectively. 
    It is also through these State Attributes that we can calculate an agent's well-being.
    """
    
    #==================================================[Initialization]==================================================
    def __init__(self):
        """
        Initializes the agent's attributes
        """
        #Fetch Configurations
        attribute_config = {}
        targetDir = os.path.join(os.path.dirname(__file__), 'Utils\\attributes.json')
        with open(targetDir) as f:
            attribute_config = json.load(f)
        
        # Initialize the attributes dictionary from the settings
        self.attributes = {
            attribute_name: Attribute(
                description=details["description"],
                value=details["actions"],
                initial_value=details.get("benefits"),
                min_value=details.get("maxDuration"),
                max_value= details.get("max_value"),
                optimal_value= details.get("optimal_value")
        )
        for attribute_name, details in attribute_config.items()
        }

        # Track the last time the attributes were updated
        self.last_updated = time.time()
        
    #==================================================[Core methods]==================================================
    def Modify(self, attribute_name, value):
        """
        Modifies the value of an attribute by a given amount.
        
        :param attribute_name: The name of the attribute to modify.
        :param value: The amount to modify the attribute by.
        """
        attribute = self.attributes.get(attribute_name)
        if not attribute:
            return False
        attribute['value'] = math.max(attribute., min(value, maximum))
        return True
    
    
    #==================================================[Utility methods]==================================================
