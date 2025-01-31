--[[
Handles the creation and management of genes, 
genes are created dynamically and are NOT predefined. 
This approach allows for the emergence of completely unique genes
outside the influence of the programmer (i) or anyone else.
]]
local SS = game:GetService("ServerStorage")
local Components = SS:WaitForChild("Components")
local Utils =require(SS.Utils)
local Attributes = require(Components.Minor.Attributes)

local Gene = {}
Gene.__index = Gene


function Gene.new()
	local newGene:Utils.Gene = {}
	setmetatable(newGene, Gene)
	
	newGene.attribute = Attributes.getRandom()
	newGene.isActive = false
	newGene.effectApplied = false
	newGene.type = math.random(0.1,1.0) > 0.5 and 'Weight' or 'Decay'
	newGene.value = math.random(-Utils.SimulationSettings.GeneValueRange,Utils.SimulationSettings.GeneValueRange )
	newGene.name = newGene.attribute..`{newGene.type}.._Gene`
	
	newGene.baseActivationThreshold = math.random(0.1,1.0) --the genes sensitivity in a sense, values closer to zero are easier to activate
	newGene.conditionals = Gene.generateConditionals(Utils.SimulationSettings.ConditionalRange)
	newGene.influences = {} --Empty for now TODO:AddInfluences
	newGene.minThreshold = 0 --Represents the point in which our gene is active
	newGene.maxThreshold = 10 --The max possible value a gene can reach, in a sense how weak a gene can get	
	
	return newGene
end


function Gene:UpdateActiveStatus(Brain:Utils.Brain)
	
	local totalThreshold = self.baseActivationThreshold
	
	--Calculate conditional value change (based on active conditions)
	local conditionalValueChange = 0
	for _,conditional:Utils.GeneCondition in self.conditionals do
		local ValueA = Brain.Body.get_attr_value(self.attribute)
		local ValueB = (type(conditional.value) == 'string') and Brain.Body.get_attr_value(conditional.value) or conditional.value
		local conditionMet = Utils.conditionalFunction[conditional.operator](ValueA,ValueB)
		if(conditionMet) then
			conditionalValueChange += conditional.thresholdChange
		end
	end
	
	self.isActive = math.max(0,totalThreshold - conditionalValueChange) == 0
	Utils.handleGeneEffect[self.type](Brain,self)
end

function Gene:ApplyEffect()
	
end
function Gene:RemoveEffect()
	
end

function Gene.generateConditionals(totalConditionals:number)
	local range = math.sqrt(75/totalConditionals)
	local conditionals = {}
	
	
	for i=0,totalConditionals do 
		local thresholdEffect = (math.random(0.0,1.0)*2*totalConditionals)-totalConditionals
		local geneConditional:Utils.GeneCondition = {
			targetAttribute = require(Components.Minor.Attributes).getRandom(),
			operator = Utils.Operators[math.random(#Utils.Operators)],
			value = math.random(0.0,1.0) > 0.5 and require(Components.Minor.Attributes).getRandom() or math.random(0,10), --Second parameter can be attribute or value
			thresholdChange = thresholdEffect
		}
	end
	
	return totalConditionals
end

return Gene
