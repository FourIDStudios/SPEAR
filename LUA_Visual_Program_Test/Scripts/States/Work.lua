local SS = game:GetService("ServerStorage")
local Utils =require(SS.Utils)


local State:Utils.State = {}
State.Name = script.Name
--Benefits is a loose term here as it holds both the cost and benefits
State.Benefits = {
	Energy = -1.0,     -- Work consumes energy
	Resources = 3.0,   -- Earn money/resources
	Mood = -1.0,        -- Slight decrease in mood due to work stress
	Hunger = -0.75,     -- Gets hungry while working
	Health = -0.5       -- Slight health decrease (sedentary work)
}
State.Location = 'Work'
State.DecayRate = nil
State.MaxDuration = nil
State.Conditions = {}
State.isTransitioning = false
State.transitionProgress = 0
State.transitionCost = 0
State.transitionStarted = false

--When transitioning we can set transition cost, and validate it against progress to check if we've entered the state?

function State.isAccessible(Brain:Utils.Brain) --Determines if the state is accesible
	
	if(Brain.CurrentState.Name == script.Name) then  return false end --Already in state
	
	return true
end

function State.canRemain(Brain:Utils.Brain)
	return Brain.Body:get_attr_value("Energy") > 0
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
	Brain.Body.Location = State.Location
	--Gains one tick worth (immediate rewards)
	Brain.Body:modify_attribute(State.Benefits)
end

function State.Tick(Brain:Utils.Brain) --Our tick function for state logic
	if State.isTransitioning then
		local AgentChar = Brain.Body.Character
		if(not State.transitionStarted) then
			local AgentHum:Humanoid = AgentChar.Humanoid
			State.transitionCost = math.abs((AgentChar.PrimaryPart.Position - workspace.Work_Location.Position).Magnitude)
			Brain:MoveTo(workspace.Work_Location)
			State.transitionStarted = true
		end
		
		--Update progress based on distance from target
		local DistanceToWork = math.abs((AgentChar.PrimaryPart.Position - workspace.Work_Location.Position).Magnitude)
		State.transitionProgress = (State.transitionCost-DistanceToWork)/State.transitionCost
		if State.transitionProgress >= .92 then --A small margin of error is proveded
			State.OnTransitioned(Brain)
		end
	else
		print(`[X][STATE][{Brain.Body.Name}]: Tick!`)
		print(State, State.Benefits)
		Brain.Body:modify_attribute(State.Benefits)
	end
end

function State.calculateTransition(Brain:Utils.Brain) --Used to calculate transition cost to state
	--Calculate distance to work location
	local TargetLocation = workspace.Work_Location

	--Modify value based on happiness, assuming an agent is more willing to work if happy
	return math.abs((Brain.Body.Character.PrimaryPart.Position - TargetLocation.Position).Magnitude)
end


return State
