local SS = game:GetService("ServerStorage")
local Components = SS:WaitForChild("Components")
local Utils =require(SS.Utils)


local Agent = {}
Agent.__index = Agent

function Agent.new(Name:string, DefaultValues:{string:any}?):Utils.Agent
	local newAgent:Utils.Agent = {}
	setmetatable(newAgent, Agent)
	
	--Create new agent
	newAgent.Name = Name
	newAgent.Body = require(Components.Major.Body).new(Name)
	newAgent.Brain = require(Components.Major.Brain).new(newAgent.Body)

	return newAgent
end

--Ticks the current agents state, similar to the agent 'Thinking'
function Agent:Tick() --The Agent Thinking in a sense
	--Tick State
	task.spawn(function()
		self.Brain:Tick()
	end)
end

return Agent

