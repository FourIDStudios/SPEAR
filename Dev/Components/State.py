import time

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
    def evalute_and_act(self):
        """
        Evaluates possible actions and decides the next action to perform.

        :return: The chosen action or 'continue' if no transitions are preferred.
        """
        if not self.action_list:  # No actions to take
            return "continue"
        # Example: Prioritize the first action in the action list for now
        # return list(self.action_list.keys())[0]
        return "continue"
    
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


        