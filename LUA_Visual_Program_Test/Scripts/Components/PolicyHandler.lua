--[[
Contains and handles policy logic such as policy optimization
]]
local SS = game:GetService("ServerStorage")
local Components = SS:WaitForChild("Components")
local Utils =require(SS.Utils)

--I will attempt a Q learning policy
local PolicyHandler = {}
PolicyHandler.__index = PolicyHandler
PolicyHandler.Settings = 
	{
		LearningRate = 0.1,
		DiscountRate = 0.9,
		DiscoveryRate = 0.3,
	}


--Variables & References
PolicyHandler.PrevState = nil

--Our memory in a sense, our decision matrix if you would
PolicyHandler.QValues = {}

--[[
Because i want to create multiple agents in the future that can learn in parrallel or otherwise,
i took an object based approach to creating the policy/policy handler
]]
function PolicyHandler.New()
	local newPolicyHandler = {}
	setmetatable(newPolicyHandler, PolicyHandler)

	-- Copy the predefined PolicyHandler into the newPolicyHandler instance
	for key, value in pairs(PolicyHandler) do
		if type(value) == "table" and value.value then
			newPolicyHandler[key] = table.clone(value) -- Clone to avoid shared references
		end
	end

	return newPolicyHandler
end

--[[
This returns our bestaction, in the context of our system there is
some "exploration" value that allows the agent to try new options and not just default
to the first positive action it finds, I'm still learning what a good exploration value is 
that allows it to focus on choosing the right option a sufficient amount of time whilst still 
having enough lee-way to find that optimized path
]]
function PolicyHandler:GetAction(Brain:Utils.Brain)
	local currentState = Brain:GetPolicyState(Brain.CurrentState)
	local Actions = PolicyHandler.QValues[currentState]
	print(Actions)
	if(not Actions) then
		Actions = Brain:GetPossibleActions()
		self.QValues[currentState] = Actions
	end
	
	--Choose best action or a change at exploring a random one
	if(math.random() < self.Settings.DiscoveryRate) then
		--Generate a list of possible actions
		local possibleActions = {}
		for i,v in Actions do
			table.insert(possibleActions, i)
		end
		--select a random one and return it
		local action = possibleActions[math.random(#possibleActions)]
		print("Exploring Action: ",action)
		return action
	else
		--Select The action with the highest MaxQ
		local bestaction,maxQ = self:GetMaxQ(currentState)
		print("Best Action: ",bestaction, maxQ)
		return bestaction
	end
	
end

--[[
This function should update the Q-Values, over time with a score relative to 
it's benefit, this is in a sense how we converge the values and fill out our Q-values chart

]]
function PolicyHandler:UpdateValues(State:Utils.PolicyState,Action:string,reward:number,nextState)
	
	--Check|Create state-action pairs
	if not self.QValues[State] then self.QValues[State] = {} end
	if not self.QValues[State][Action] then self.QValues[State][Action] = 0 end
	
	--Get the max Q-Value for the next state
	local action,maxNextQ = self:GetMaxQ(nextState)
	
	
	--[[
	This is the q learning function to explain it in the way i understand it
	It can be represented as
	currenQ + alpha(learning rate) * (reward + gamma(discount rate) * maxNextQ - currentQ)
	
	This basically updates the current QValue based on the award the agent recieved from taking the action, 
	plus the difference between the qValue of the next state and the current state>

	The following are notes for myself to better understand this
	
	currentQ -> is our old q value (its important to remeber that we are in the process of transitioning to a new state at this point)
	
	reward -> is our immediate rewards, so what the agent will recieve as soon as they take this action/go to this nextState
	
	maxNextQ -> is the best possible future QValue basically the best rewards we can recieve from the nextState
	
	discountRate(gamma) -> How much we care about future rewards, how heavily the possibility of a better future state affects the current state in a sense, the higher this rate
	the more the agent will care about longterm/future rewards
	
	learningRate(alpha) -> controls how much the qvalues change, which is in a sense how quickly it changes, with lower values it takes longer to converge on a value but its usually more accurate
	lets take for example a alpha of 1, if the agent gets some super rare reward that gives really good outcomes. it will retain this value and keep trying to make this decision which would not 
	be the desired result, a lower value leads to slower learning yes, but in turn we can avoid situations where extreme values "lock" us out of an "optimal" value
	]]
	self.QValues[State][Action] = 
		self.QValues[State][Action] + self.Settings.LearningRate * 
		(reward + self.Settings.DiscountRate * maxNextQ - self.QValues[State][Action])
	
	print(`\n------------------------------------`)
	print('QValues:',self.QValues)
	print(`------------------------------------\n`)

end



--[[
We can use this function to fetch the MaxQ value in a state, this
way we can determine our "best" action, since not all our q values are initially 
filled out we can return zero here, now we return both state and q value
but depending on the context this function is used in we might only need q value. 
(this is why our default returns nil,0 if that presented any confusion)

]]

function PolicyHandler:GetMaxQ(State:Utils.PolicyState)
	--Check for any possible QValue or return 0
	if not self.QValues[State] then print("No State For Max Q") return nil,0 end
	
	--Search for the best action in state
	local maxQ = -math.huge
	local bestaction = nil
	for action,qValue in self.QValues[State] do
		if(qValue > maxQ) then 
			maxQ = qValue
			bestaction = action 
		end
	end
	
	return bestaction,maxQ
	
end




return PolicyHandler
