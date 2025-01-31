local SS = game:GetService("ServerStorage")
local Utils =require(SS.Utils)


local State:Utils.State = {}
State.Name = script.Name
--Benefits is a loose term here as it holds both the cost and benefits
State.Benefits = {
	Energy = 5.0,      --Significant energy recovery
	Resources = -0.1,   --Minimal resource consumption
	Mood = 1.5,        --Mood improvement from good rest
	Hunger = -0.3,     --Gets slightly hungry over time
	Health = 1.0       --Health recovery from rest
}
State.Location = 'World'
State.DecayRate = nil
State.CurrentDuration = 0
State.MaxDuration = 10
State.Conditions = {}
State.isTransitioning = false
State.transitionProgress = 0
State.transitionCost = 0
State.transitionStarted = false
State.lastEntered = -math.huge
State.timeBetweenStates = 30

--When transitioning we can set transition cost, and validate it against progress to check if we've entered the state?

function State.isAccessible(Brain:Utils.Brain) --Determines if the state is accesible
	
	if(Brain.CurrentState.Name == script.Name) then  return false end --Already in state
	
	return true
end

function State.canRemain(Brain:Utils.Brain)
	return State.CurrentDuration < State.MaxDuration
end

function State.canExit(Brain:Utils.Brain) --Determines if the state is currently Unexitable
	return true
end

function State.OnExit(Brain:Utils.Brain)
	return
end

function State.OnTransitioned(Brain:Utils.Brain) --Fired when the agent has finished transitioning
	State.isTransitioning = false
	State.transitionProgress = 0
	State.transitionCost = 0
	State.transitionStarted = false
	State.CurrentDuration = 0
	State.lastEntered =  time()
	Brain.Body.Location = "World"
	
	--Gains one tick worth (immediate rewards)
	Brain.Body:modify_attribute(State.Benefits)
	return
end

function State.Tick(Brain:Utils.Brain) --Our tick function for state logic
	if State.isTransitioning then
		local TargetLocation = workspace.Rest_Location
		local AgentChar = Brain.Body.Character
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
		if(State.MaxDuration) then
			State.CurrentDuration += 1
		end
		Brain.Body:modify_attribute(State.Benefits)
	end
end

function State.calculateTransition(Brain:Utils.Brain) --Used to calculate transition cost to state
	--Calculate distance to work location
	local TargetLocation = workspace.Rest_Location

	--Modify value based on happiness, assuming an agent is more willing to work if happy
	return math.abs((Brain.Body.Character.PrimaryPart.Position - TargetLocation.Position).Magnitude)
end


return State
