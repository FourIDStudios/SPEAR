import time
import os
import json
import math

from Components.Genome import Genome


class Attribute:
    """
    Represents a single attribute of an agent.
    """
    def __init__(self, description, value, min_value=None, max_value=None, optimal_value=None, genomicInfluence = None):
        """
        Initializes the attribute.
        """
        self.description = description
        self.value = value
        self.min_value = min_value
        self.max_value = max_value
        self.optimal_value = optimal_value
        
        #Represents Genomic Influence on the attribute, i.e what gene and how much it influences the attribute
        self.genomicInfluence = genomicInfluence
        pass
    
    def __repr__(self):
        return f"Attribute(description={self.description}, value={self.value}, min_value={self.min_value}, max_value={self.max_value}, optimal_value={self.optimal_value}, genomicInfluence={self.genomicInfluence})"

        
    
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
        targetDir = os.path.join(os.path.dirname(__file__), '..', 'Utils', 'attributes.json')

        with open(targetDir) as f:
            attribute_config = json.load(f)
        
        # Initialize the attributes dictionary from the settings
        self.attributes = {
            attribute_name: Attribute(
                description=details["description"],
                value=details["initial_value"],
                min_value=details.get("min_value"),
                max_value= details.get("max_value"),
                optimal_value= details.get("optimal_value"),
                genomicInfluence = details.get("influence_genes")
        )
        for attribute_name, details in attribute_config.items()
        }

        # Track the last time the attributes were updated
        self.last_updated = time.time()
        
    #==================================================[Core methods]==================================================
    def modify(self, genome:Genome, attribute_name:str, value:float):
        """
        Modifies the value of an attribute by a given amount.
        
        :param attribute_name: The name of the attribute to modify.
        :param value: The amount to modify the attribute by.
        """
        
        # Fetch necessary information from the agent
        agentGenome = genome
        
        # Ensure the attribute exists
        attribute:Attribute = self.attributes.get(attribute_name)
        if not attribute or not agentGenome:
            return False
        
        # Update the attribute value, ensuring it stays within the min/max bounds with the genomic influence
        attribute.value = max(attribute.min_value, min(attribute.value+value, attribute.max_value))
        
        # Check for genomic influence (Gain or Drain) i.e AmbitionGain, AmbitionDrain
        for geneName, influence in attribute.genomicInfluence.items():
            if(str.endswith(geneName, "Gain")):
                #Check if the gene is present in the genome
                geneInfo = agentGenome.getGene(geneName)
                if not geneInfo or geneInfo == None:
                    continue
                gainAmount = value * (influence * geneInfo.get('value'))
                attribute.value = max(attribute.min_value, min(attribute.value+gainAmount, attribute.max_value))
            elif(str.endswith(geneName, "Drain")):
                #Check if the gene is present in the genome
                geneInfo = agentGenome.getGene(geneName)
                if not geneInfo or geneInfo == None:
                    continue
                drainAmount = value * (influence * geneInfo.get('value'))
                attribute.value = max(attribute.min_value, min(attribute.value-drainAmount, attribute.max_value))
        
        return True
    
    def get(self, attribute_name):
        """
        Retrieves an attribute by name.
        
        :param attribute_name: The name of the attribute to retrieve.
        :return: The attribute object.
        """
        return self.attributes.get(attribute_name)
    
    def getValue(self, attribute_name):
        """
        Retrieves the value of an attribute.
        
        :param attribute_name: The name of the attribute to retrieve.
        :return: The value of the attribute.
        """
        # Ensure the attribute exists
        attribute:Attribute = self.attributes.get(attribute_name)
        if not attribute:
            return None
        
        return attribute.value
    
    def getWellBeing(self):
        """
        Calculates the agent's well-being based on the current attribute values.
        These values are compared to the optimal values to determine the agent's overall well-being.
        
        :return: The agent's well-being as a percentage.
        """
        # Calculate the total well-being based on the difference between the current and optimal values
        total_difference = sum(abs(attribute.value - attribute.optimal_value) for attribute in self.attributes.values())
        total_possible_difference = sum(abs(attribute.max_value - attribute.min_value) for attribute in self.attributes.values())
        
        # Calculate the well-being as a percentage
        return 100 - (total_difference / total_possible_difference) * 100
    
    #==================================================[Utility methods]==================================================
