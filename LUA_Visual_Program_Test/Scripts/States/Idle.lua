local SS = game:GetService("ServerStorage")
local Utils =require(SS.Utils)


local State:Utils.State = {}

State.Name = script.Name
State.Benefits = {
	Energy = -0.1,     -- Very slow energy drain
	Resources = -0.2,   -- Small resource consumption (passive spending)
	Mood = 1.0,        -- Slight mood improvement from relaxation
	Hunger = -0.5,     -- Gets slightly hungry over time
	Health = 0.0       -- No significant health impact
}
State.Location = 'World'
State.DecayRate = nil
State.MaxDuration = nil
State.Conditions = {}
State.isTransitioning = false
State.transitionProgress = 0
State.transitionCost = 0

--When transitioning we can set transition cost, and validate it against progress to check if we've entered the state?

function State.isAccessible(Brain:Utils.Brain) --Determines if the state is accesible
	if(Brain.CurrentState.Name == script.Name) then return false end --Already in state

	return true
end

function State.canRemain(Brain:Utils.Brain)
	return true
end

function State.canExit(Brain:Utils.Brain) --Determines if the state is currently Unexitable
	return true
end

function State.OnTransitioned(Brain:Utils.Brain) --Fired when the agent has finished transitioning
	State.isTransitioning = false
	State.transitionProgress = 0
	State.transitionCost = 0
	State.transitionStarted = false
	Brain.Body.Location = "World"
	--Gains one tick worth (immediate rewards)
	Brain.Body:modify_attribute(State.Benefits)
end

function State.OnExit(Brain:Utils.Brain)
	return
end

function State.Tick(Brain:Utils.Brain) --Our tick function for state logic
	if State.isTransitioning then
		local AgentChar = Brain.Body.Character
		local TargetLocation = workspace.Idle_Location
		if(not State.transitionStarted) then
			local AgentHum:Humanoid = AgentChar.Humanoid
			State.transitionCost = math.abs((AgentChar.PrimaryPart.Position - TargetLocation.Position).Magnitude)
			Brain:MoveTo(TargetLocation)
			State.transitionStarted = true
		end

		--Update progress based on distance from target
		local DistanceToWork = math.abs((AgentChar.PrimaryPart.Position - TargetLocation.Position).Magnitude)
		State.transitionProgress = (State.transitionCost-DistanceToWork)/State.transitionCost
		if State.transitionProgress >= .92 then --A small margin of error is proveded
			State.OnTransitioned(Brain)
		end

	else
		
		Brain.Body:modify_attribute(State.Benefits)
	end
end

function State.calculateTransition(Brain:Utils.Brain) --Used to calculate transition cost to state
	--Calculate distance to work location
	local TargetLocation = workspace.Idle_Location

	--Modify value based on happiness, assuming an agent is more willing to work if happy
	return math.abs((Brain.Body.Character.PrimaryPart.Position - TargetLocation.Position).Magnitude)/50
end

return State
