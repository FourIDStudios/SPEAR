local SS = game:GetService("ServerStorage")
local Components = SS:WaitForChild("Components")
local Utils =require(SS.Utils)

local Brain = {}
Brain.__index = Brain
Brain.States = {}
Brain.NavParams = 
	{
		BrainRadius = 3,
		BrainHeight = 5,
		BrainCanJump = true,
		BrainCanClimb = true, 
		WaypointSpacing = 6
	}
Brain.Pathfind = require(Components.Minor.SimplePath)
Brain.Policy = require(Components.Parent.PolicyHandler).New()
Brain.PathListeners =  {}


--[[

	This Class acts as the FSM(Finite State Machine) Controller,
	that handles all of our state logic, this is the brain of the Agent which
	is to say, it handles all of the agents actions.

	:param Body: The body of the agent, this contains all of the agents information
	:param DefaultValues: A dictionary of overide values (Optional)

]]
function Brain.new(Body:Utils.Body, DefaultValues:{string:any}?)
	--Create new Brain
	local newBrain = {}
	setmetatable(newBrain, Brain)
	
	--Assign Components
	newBrain.Body = Body
	
	--Fetch States
	for _,State in SS.States:GetChildren() do
		local state = require(State)
		newBrain.States[string.lower(state.Name)] = state
	end

	--Set initial state
	newBrain.CurrentState = newBrain.States['idle']

	--Populate data with any default values given
	if(DefaultValues) then
		for Key,value in DefaultValues do
			newBrain[Key] = value
		end
	end

	print(`[X][Brain][{newBrain.Body.Character.Name}'s Brain Initialized']: W|Data ->  `,newBrain)

	return newBrain
end

--Ticks the current Brains state, similar to the Brain 'Thinking'
function Brain:Tick() --The Brain Thinking in a sense
	print(`[X][Brain][{self.Body.Name}]: Current State : `,self.CurrentState.Name)
	print(`State:`,self.Body.Attributes,self.Body.Attributes.Energy)
	
	--Check for Transitioning (if so Tick state)
	if(self.CurrentState.isTransitioning) then
		print('transitioning...')
		task.spawn(function()
			self.CurrentState.Tick(self)
		end)
		return
	end

	--Check if the Brain can exit current state
	if(self.CurrentState.canExit(self)) then
		--Calculate wellness for current state
		local MaintainStateScore = self.Body:getWellbeing()
		if(not self.CurrentState.canRemain(self)) then MaintainStateScore = -math.huge end
		print(`[X][Brain][{self.Body.Name}]: Maintain State Score: `,MaintainStateScore)
		

		--Calculate Policy Parameters
		local currentPolicyState = self:GetPolicyState(self.CurrentState)
		local nextAction = string.lower(self.Policy:GetAction(self))
		local NextBestState = self.States[nextAction]
		local reward = self.Body:getWellbeing(NextBestState.Benefits)-NextBestState.calculateTransition(self)
		local nextPolicyState = self:GetPolicyState(self.States[nextAction])
		
		--Update Policy Values
		self.Policy:UpdateValues(currentPolicyState,nextAction,reward,nextPolicyState)
		
		--Check for transition to new state
		if(NextBestState ~= self.CurrentState) then
			--Transition to the next state
			self.CurrentState.OnExit(self)
			self.CurrentState = self.States[nextAction]
			self.CurrentState.transitionCost = self.CurrentState.calculateTransition(self)
			self.CurrentState.isTransitioning = true
		end
	end

	--Tick State
	task.spawn(function()
		self.CurrentState.Tick(self)
	end)
end

function Brain:MoveTo(TargetCFrame:CFrame, visualize:boolean)
	if(not visualize) then
		visualize = true
	end

	--Testing
	local PlayerChar:Model = self.Body.Character
	PlayerChar.PrimaryPart.CFrame = TargetCFrame.CFrame

	----Define MoveToGoal
	--local GoalPosition = TargetCFrame

	----Create Path
	--self.Path = self.Pathfind.new(self.Body.Character, self.NavParams)
	--self.Path.Visualize = visualize

	----Clear old path listners
	--self:MoveToClear()

	--local GoalReached = self.Path.Reached:Connect(function()
	--	self.CurrentState.OnTransitioned(self)
	--end)

	--local BlockedEvent = self.Path.Blocked:Connect(function()
	--	self.Path:Run(GoalPosition)
	--end) table.insert(self.PathListeners,BlockedEvent)

	--local ErrorEvent = self.Path.Error:Connect(function(errorType)

	--	self.Path:Run(GoalPosition)
	--end) table.insert(self.PathListeners,ErrorEvent)

	--self.Path:Run(GoalPosition)

end

function Brain:MoveToClear()
	if(self.PathListeners) then
		for _,listener in self.PathListeners do
			listener:Disconnect()
		end
	end
end

function Brain:GetPolicyState(State:Utils.State)
	local PolicyState:Utils.PolicyState = {}
	PolicyState.State = State.Name
	PolicyState.Location = State.Location
	PolicyState.Health = Utils.AttributeToStateValue(self.Body:get_attr('Health'),State.Benefits['Health'])
	PolicyState.Hunger = Utils.AttributeToStateValue(self.Body:get_attr('Hunger'),State.Benefits['Hunger'])
		PolicyState.Energy = Utils.AttributeToStateValue(self.Body:get_attr('Energy'),State.Benefits['Energy'])
	PolicyState.Mood = Utils.AttributeToStateValue(self.Body:get_attr('Mood'),State.Benefits['Mood'])
	PolicyState.Resources = Utils.AttributeToStateValue(self.Body:get_attr('Resources'),State.Benefits['Resources'])
	
	local GeneratedState = Utils.StateToString(PolicyState)
	return GeneratedState
end

function Brain:GetPossibleActions()
	--Calculate Possible States
	local PossibleStates = {}
	for stateName,state:Utils.State in self.States do
		if(state.isAccessible(self)) then
			PossibleStates[stateName] = 0
		end
	end
	--Staying is always an option
	PossibleStates[self.CurrentState.Name] = 0
	
	return PossibleStates
end


return Brain

