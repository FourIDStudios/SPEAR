local SS = game:GetService("ServerStorage")
--[FiniteStateManagement]
export type State = 
	{
		Benefits:{string:number},
		DecayRate:number,
		MaxDuration:number?,
		Conditions:{string:any},
		isTransitioning:boolean,
		transitionProgress:number,
		transitionCost:number,
		Location:string,
		
		isAccessible:(any)->boolean, --Determines if the state is accesible
		canExit:(any)->boolean, --Determines if the state is accesible
		calculateTransition:()->number, --Used to calculate transition cost to state
		
		Tick:()->(), --Our tick function for state logic
		
	}

--[Agent Components]
export type Agent = 
	{
		Name:string, 
		Brain:Brain,
		Body:Body,
		
		Tick:()->(),
	}

export type Brain = 
	{
		CurrentState:State,
		States:{string:State},
		Body:Body,
		
		Tick:()->(),
		MoveTo:()->(),
		MoveToClear:()->(),
		GetPolicyState:()->PolicyState,
	}

export type Body = 
	{
		Character:Model, 
		Attributes:{Attribute},
		Location:string,
		
		getWellbeing:()->(),
		get_attr:(string,number)->Attribute,
		get_attr_value:(string,number)->number|nil,
		modify_attribute:(string,number)->boolean,
	}

--[Minor Components]
export type Attribute = 
	{
		description:string, 
		
		value:number, 
		min_value:number,
		max_value:number, 
		optimal_value:number,
		
		--Weight
		base_weight:number,
		weight:number,
		
		--Value from -1,1, that determines the increase/decrease of X attribute per tick
		decay_rate:number?, 
		
		--TODO:AddGenomes
		genomic_influence:{string:number}?,
	}
export type Gene = 
	{
		attribute:string,
		name:string,
		value:number,
		baseActivationThreshold:number,
		conditionals:{GeneCondition},
		influences:{GeneInfluence},
		isActive:boolean,
		effectApplied:boolean,
		minThreshold:number, 
		maxThreshold:number,
		type:GeneType,
		
		evalute:()->(), --Evalutes the Genes State
		checkConditionals:(GeneCondition)->(), --Abjust the states threshold based on the current state of the agent
		getFinalThreshold:()->(), --Calculates the final threshold requirement for activation based on conditionals and influences
	}
--GeneConditions are conditional statements that modifie a genes activation threshold when evaluated to be active
export type GeneCondition =  
	{
		targetAttribute:string,
		operator:Operator,
		value:number|string,
		thresholdChange:number
	}
export type GeneType = "Weight"|"Decay"


--GeneInfluence is a rule that adjusts the threshold of a gene based on the activity (active/inactive state) of another gene.
export type GeneInfluence = 
	{
		
	}


--[Enums]
export type Operator = ">"|"<"|">="|"<="|"=="


--[MDP & Policy]
export type PolicyState = {
	State:string, 
	Health:number,
	Energy:number,
	Hunger:number,
	Mood:number,
	Resources:number,
	Location:string,
}
export type DiscreteRanges = "Critical"|"Low"|"Normal"|"Optimal"

local Utils = {}

--[Settings]
Utils.SimulationSettings = 
	{
		ConditionalRange = 3,
		GeneValueRange = 5,
		TickRate = .001, 
	}

--[Lists]
Utils.Operators = {">","<",">=","<=","=="}


--[Functions]
Utils.handleGeneEffect = {
	['Weight'] =function(Brain:Brain, gene:Gene)
		if(gene.isActive and not gene.effectApplied) then
			--Enable Effect
			Brain.Body.Attributes[gene.attribute].base_weight += gene.value
			
		elseif(not gene.isActive and gene.effectApplied) then
			--Disable Effect
			Brain.Body.Attributes[gene.attribute].base_weight -= gene.value
		end
	end,
	['Decay'] =function(Brain:Brain, gene:Gene)
		if(gene.isActive and not gene.effectApplied) then
			--Enable Effect
			Brain.Body.Attributes[gene.attribute].base_weight += gene.value

		elseif(not gene.isActive and gene.effectApplied) then
			--Disable Effect
			Brain.Body.Attributes[gene.attribute].base_weight -= gene.value
		end
	end,
}
Utils.conditionalFunction = {
	[">"] = function (number1,number2) 
		return number1>number2 
	end;
	["<"] = function (number1,number2) 
		return number1<number2 
	end;
	[">="] = function (number1,number2) 
		return number1>=number2 
	end;
	["<="] = function (number1,number2) 
		return number1<=number2 
	end;
	["=="] = function (number1,number2) 
		return number1==number2 
	end;
}
--[MDP & Policy]
Utils.StateMapping = {}
function Utils.GetStateMappings ()
	local States = #Utils.StateMapping > 0 and Utils.StateMapping or false
	if(not States) then
		local allStates = SS.States:GetChildren()
		for _,state in allStates do
			table.insert(Utils.StateMapping,state.Name)
		end
	end
end

function Utils.StateToString(State:PolicyState)
	return `{State.State}|{State.Location}:{State.Health},{State.Hunger},{State.Energy},{State.Mood},{State.Resources}`
end
function Utils.AttributeToStateValue(Attr:Attribute, Modifier:number)
	if(not Modifier) then Modifier = 0 end
	--Define thresholds, optimal is anything outside this range
	local critical = Attr.min_value + 0.25 * (Attr.optimal_value - Attr.min_value)
	local low = Attr.optimal_value - 0.25 * (Attr.optimal_value - Attr.min_value)
	local nominal = Attr.optimal_value + 0.25 * (Attr.max_value - Attr.optimal_value)
	
	local attrValue = math.clamp(Attr.value+Modifier,Attr.min_value,Attr.max_value)
	if(attrValue <= critical) then return "Critical"
		elseif(attrValue <= low) then return "Low"
		elseif(attrValue <= nominal) then return "Normal"
	else return "Optimal" end

end

--generate a weighted result, where the minimum is the most lightest element, and the maximum the heavy
function Utils.weightedRandom(min, max) 
	return max - math.round(max / (math.random() * max + min));
end

return Utils
