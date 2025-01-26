import copy
import time
import os
import json

from Components.Body import Body


#Fetch Configurations
state_config = {}
targetDir = os.path.join(os.path.dirname(__file__), '..', 'Utils', 'states.json')

with open(targetDir) as f:
    state_config = json.load(f)
    
# Create StateInfo Table from the configuration
States = {
    state_name: {
        "name": state_name,
        "actionList": details["actions"],
        "benefits": details.get("benefits"),
        "maxDuration": details.get("maxDuration")
    }
    for state_name, details in state_config.items()
}


class State:
    """
    Represents a state in the FSM(Brain).
    """
    
    #==================================================[Initialization]==================================================
    def __init__(self, name, actionList=None, benefits=None, maxDuration=None):
        """
        Represents a state in the FSM.

        :param name: Name of the state.
        :param action_list: Dictionary of actions -> next possible states.
        :param benefits: Optional dictionary defining the benefits of being in this state.
        :param duration: Optional duration to define how long the agent can remain in the state.
        """
        self.name = name
        self.action_list = actionList or {}      # Actions -> next states
        self.benefits = benefits or {}          # State-specific benefits
        self.max_duration = maxDuration or 0  # Duration can be 0 if unlimited
        self.remaining_duration = self.max_duration  # Track remaining time
        self.last_entered = None  # Track when this state was last entered
        
    #==================================================[Core methods]==================================================
    def evalute_and_act(self, body:Body): #Requires a snapshot of the current state of the agent
        """
        Evaluates possible actions and decides the next action to perform. based
        on conditional logic.

        :return: The chosen action or 'continue' if no transitions are preferred.
        """
        
        """"
        Takes a look at the benefits form the variouse states and decides which state to transition to
        based on which state results in a higher well-being for the agent
        """
        
        if not self.action_list:  # No actions to take
            return "continue"
        
        #Get the current state of the agent
        Current_Wellbeing_score = body.attributes.getWellBeing()
        
        #Get a copy of the body of the agent (copy of the attribute object)
        Current_Body = copy.deepcopy(body.attributes)
        
        #Iterate through the possible actions and calculate the well-being of the agent in each state
        Possible_States = []
        for action in self.action_list:
            Next_State = States[self.action_list[action]]
            Next_State_Benefits = Next_State.get('benefits') #{Money:10, Health: -1}
            
            #Iterate overz the benefits of the next state and calculate the well-being of the agent
            for benefit, value in Next_State_Benefits.items():
                
                #Ensure the benefit exists in the current well-being (shouldn't be possible but just in case)
                if(Current_Body.get(benefit) == None):
                    continue
                #Modify the current well-being of the agent
                Current_Body.modify(body.genome, benefit, value)
            
            #Store the well-being of the agent in the next state (name,wellbeing)
            Possible_States.append((action,Current_Body.getWellBeing()))
        
        #Find the state that results in the highest well-being for the agent
        Best_Action = {
            "Action":'continue',
            "Wellbeing":Current_Wellbeing_score
        }
        
        #Iterate through the possible states and find the state that results in the highest well-being for the agent
        for Action,Wellbeing in Possible_States:
            if(Best_Action["Action"] == None): #Shouldn't be possible but just in case
                Best_Action["Action"] = Action
                Best_Action["Wellbeing"] = Wellbeing
            elif(Wellbeing > Best_Action["Wellbeing"]): #If the well-being of the agent in the next state is higher than the current state
                Best_Action["Action"] = Action
                Best_Action["Wellbeing"] = Wellbeing
        
        #Return the action that results in the highest well-being for the agent
        return Best_Action["Action"]
    
    def can_continue(self):
        """
        Determines whether the state can continue based on its internal logic.

        :return: True if the state can continue; False otherwise.
        """
        if self.remaining_duration is None:  # Infinite duration
            return True
        return self.remaining_duration > 0

    def on_continue(self): #TODO: Rename to 'Tick'?
        """
        Logic for the 'continue' action. Decrements duration (if applicable).
        """
        if self.remaining_duration is not None:
            self.remaining_duration -= 1
        return self.name  # Continuing in the same state

    def add_action(self, action, next_state):
        """
        Adds an action to the state's action list.

        :param action: The action (Function) that triggers a transition.
        :param next_state: The name of the next state triggered by the action.
        """
        self.action_list[action] = next_state
        
    def get_possible_actions(self):
        """
        Returns the possible actions from this state.
        """
        return list(self.action_list.keys())
    
    def reset_state(self):
        """
        Resets the state, such as its remaining duration or other properties, when re-entered.
        """
        self.remaining_duration = self.max_duration  # Reset duration
        self.last_entered = time.time()  # Optionally track last entered time
    
    #==================================================[Utility methods]==================================================
    def __repr__(self):
        return f"State(name={self.name}, action_list={self.action_list}, benefits={self.benefits}, duration={self.remaining_duration})"


        