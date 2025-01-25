import time
import os
import json
from Components.State import State
from Utils.Logger import Logger

#Fetch Configurations
state_config = {}
targetDir = os.path.join(os.path.dirname(__file__), 'Utils\\states.json')
Logger.debug = True
Logger.logln(f"[PAI][FSM]: Fetching states from {targetDir}")
with open(targetDir) as f:
    state_config = json.load(f)
    
# Create State objects from the configuration
States = {
    state_name: State(
        name=state_name,
        actionList=details["actions"],
        benefits=details.get("benefits"),
        maxDuration=details.get("maxDuration")
    )
    for state_name, details in state_config.items()
}

class Brain:
    #==================================================[Initialization]==================================================
    def __init__(self, initial_state:State, interval=1.0):
        """
        Initializes the FSM with a starting state.

        :param initial_state: The starting State object.
        """
        self.current_state:State = initial_state if initial_state else States["Resting"]
        self.interval = interval
    
    #==================================================[Core methods]==================================================
    def Think(self, action:None): #-> Transitions to the next state (if applicable)
        """
        Starts the autonomous decision-making loop.
        """
        Logger.logln("[PAI][FSM]: Starting autonomous loop.")
        try:
            while True:  # Simulate the FSM's decision-making process
                actionSuccesfull = self.process_Action()
                print(self.current_state)
                time.sleep(self.interval)  # Wait for the next interval
        except KeyboardInterrupt:
            Logger.logln("[PAI][FSM]: Autonomous loop interrupted.")

    def enter_state(self, state:State):
        """
        Enters a new state in the FSM.

        :param state: The new state to enter.
        """
        # Ensure the new state is valid
        if state not in States.values():
            Logger.logln(f"[PAI][FSM]: Invalid state '{state.name}'.")
            return 
        
        # Reset Current State (if applicable)
        if(self.current_state):
            self.current_state.reset_state()
            
        # Transition to the next state
        self.current_state = state
        self.current_state.last_entered = time.time()
        Logger.logln(f"[PAI][FSM]: Entering state '{state.name}'")
        
    def process_Action(self): #-> Transitions to the next state (if applicable)
        """
        Processes an action in the current state.

        :param action: The action to process.
        """
        
        # Evaluate the current stae's possible actions and decide the next action to perform
        action = self.current_state.evalute_and_act()
        Logger.logln(f"[PAI][FSM]: Processing action '{action}' in state '{self.current_state.name}'")
        
        # Check for Continue action, present in all states
        if action.lower() == "continue":
            if self.current_state.can_continue():
                self.current_state.on_continue()
                Logger.logln(f"[PAI][FSM]: Continuing in state '{self.current_state.name}'")
                return True
            else:
                Logger.logln(f"[PAI][FSM]: State '{self.current_state.name}' has expired.")
                return self.handle_state_expired()
            
        # Check for other possible actions in the current state
        elif action in self.current_state.get_possible_actions():
            #Fetch the next state
            next_state_name = action
            Logger.logln(f"[PAI][FSM]: Transitioning from '{self.current_state.name}' to '{next_state_name}'")
            self.enter_state(States[next_state_name])
            
            return True
        # Handle invalid actions
        else:
            Logger.logln(f"[PAI][FSM]: Invalid action '{action}' in state '{self.current_state.name}'")
            return False

    def get_CurrentState(self):
        """
        Returns the current state of the FSM.
        """
        return self.current_state
    
    def handle_state_expired(self):
        """
        Handles the situation when a state expires and the agent cannot continue.

        :return: True if a transition was successful; False otherwise.
        """
        
        # Define a fallback state (e.g., "Resting")
        fallback_state = "Resting"

        # Check if any other valid actions exist for transitioning
        possible_actions = self.current_state.get_possible_actions()
        if possible_actions:
            first_valid_action = next(iter(possible_actions))
            next_state_name = self.current_state.action_list[first_valid_action]
            Logger.logln(f"[PAI][FSM]: No fallback available. Transitioning to '{next_state_name}' via '{first_valid_action}'")
            self.enter_state(States[next_state_name])
            return True
        
        if fallback_state in States:
            Logger.logln(f"[PAI][FSM]: Transitioning to fallback state '{fallback_state}'")
            self.enter_state(States[next_state_name])
            return True

        # If no fallback or valid actions, log the failure
        Logger.logln(f"[PAI][FSM]: No valid transitions available from state '{self.current_state.name}'. Stopping.")
        return False
    
    #==================================================[Utility methods]==================================================
    def __repr__(self):
        return f"FiniteStateMachine(current_state={self.current_state})"
    


#==================================================[Testing]==================================================

# # Create Agent A with the initial state 'resting'
# AgentA = Brain(States["Resting"])

# # Start the autonomous decision-making loop
# AgentA.Think(None)