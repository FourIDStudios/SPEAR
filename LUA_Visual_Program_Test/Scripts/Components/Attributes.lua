local SS = game:GetService("ServerStorage")
local Utils =require(SS.Utils)

local Attributes =
	{
	
		['Health']={
			description = 'Represents the agents physical wellbeing',
			value = 10,
			max_value = 10,
			min_value = 0,
			optimal_value = Utils.weightedRandom(1,10),
			base_weight = 5,
			weight = 5, --Critical for survival
		},
		['Energy']= {
			description = 'Represents the agents total energy, or ability to perform tasks that require energy',
			value = 10,
			max_value = 10,
			min_value = 0,
			optimal_value = Utils.weightedRandom(1,10),
			decay_rate = -0.05,
			base_weight = 4,
			weight = 4, --Essential for most tasks
		},
		['Hunger']= {
			description = 'Represents how satisfied the agent is, where satisfaction is a measure of "lack of want to eat"',
			value = 10, 
			max_value = 10, --Full Stomach
			min_value = 0, --Starving
			optimal_value = Utils.weightedRandom(1,10),
			decay_rate = -0.1,
			base_weight = 4,
			weight = 4, --Essential for well being
		},
		['Mood']= {
			description = 'Represents the agents current mood, (-10,-5):Sad (-5,0):Dejected (0,5):Content (5:10):Happy ',
			value = 10,
			max_value = 10,
			min_value = 0,
			optimal_value = Utils.weightedRandom(1,10),
			decay_rate = -0.1,
			base_weight = 2,
			weight = 2, --moderate impact
		},
		['Resources']= {
			description = 'Respresents external things that an agent owns, that can be considered apart of the agent i.e money ',
			value = 500,
			max_value = 1000,
			min_value = 0,
			optimal_value = Utils.weightedRandom(1,1000),
			decay_rate = -1,
			base_weight = 3,
			weight = 3, --long-term stability and security. While important, they have less immediate impact
		},
	}



Attributes.__index = Attributes

function Attributes.new()
	local newAttributes = {}
	setmetatable(newAttributes, Attributes)
	
	-- Copy the predefined attributes into the newAttributes instance
	for key, value in pairs(Attributes) do
		if type(value) == "table" and value.value then
			newAttributes[key] = table.clone(value) -- Clone to avoid shared references
			task.spawn(function()
				while true do 
					--newAttributes:AbjustWeight(key)
					if(value['decay_rate']) then
						newAttributes[key].value = math.clamp(newAttributes[key].value+value['decay_rate'],newAttributes[key].min_value,newAttributes[key].max_value)
					end
					task.wait(1)
				end
			end)
		end
	end
	
	return newAttributes
end

function Attributes:__tostring()
	local result = {}
	for key, attr in pairs(self) do
		if type(attr) == "table" and attr.value then
			-- Include each attribute's name and its current value in the string
			table.insert(result, string.format("%s: %d/%d", key, attr.value, attr.max_value))
		end
	end
	return table.concat(result, ", ")
end

function Attributes:AbjustWeight(attrName)
	local attrData = self[attrName]
	if not attrData then return 1 end

	local distanceFromOptimal = math.abs(attrData.value - attrData.optimal_value)
	local maxDistance = attrData.max_value - attrData.min_value

	-- Exponential scaling for critical attributes
	-- We need a value that is high enough such that aren't always playing catchup but low enough such that its not always active
	local criticalThreshold = 0.4 -- 20% of max value
	local normalizedValue = math.abs((attrData.value - attrData.min_value) / (attrData.min_value - attrData.max_value))

	-- Calculate dynamic weight bias (simple linear scaling, can be adjusted)
	local dynamicWeight = 1 + (distanceFromOptimal / maxDistance) -- Scale the weight based on the deviation
	if normalizedValue < criticalThreshold then
		print("Critical Weight Detected On: ",attrName,normalizedValue)
		local criticalFactor = math.pow(1 - (normalizedValue / criticalThreshold), 2)
		dynamicWeight = dynamicWeight * (1 + criticalFactor * 6)
	end
	
	self[attrName].weight = attrData.weight * dynamicWeight 
end

function Attributes.getRandom()
	--Generate a list of possible attributes
	local possibleAttributes = {}
	for i,v in Attributes do
		if(typeof(v) == 'table' and i ~= '__index') then
			table.insert(possibleAttributes, i)
		end
	end
	
	--select a random one and return it
	return possibleAttributes[math.random(#possibleAttributes)]
end

Attributes.getRandom()
return Attributes