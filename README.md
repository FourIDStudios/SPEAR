#Agent-Based State Management System**

This project is a Python-based case study exploring pseudo-artificial intelligence (AI) through agent-based systems. The focus is on developing agents that interact with their environment via state transitions, evaluating their decisions to optimize well-being and simulate adaptive intelligence.
Overview

The core idea of this project is to create agents (pseudo-AI entities) capable of selecting and transitioning between various states to maximize favorable outcomes. Each agent possesses a genome, a hereditary system that influences its decision-making, behaviors, and interactions with the environment.

The system combines modular state management, cost-benefit analysis, and genetics-based adaptability to simulate complex decision-making processes.
Key Systems
1. ##Agents

Agents represent the pseudo-AI entities. Each agent:

    Has its own state (current action or focus).
    Transitions between states based on weighted decisions.
    Evaluates transition costs, rewards, and its genetic predisposition to determine optimal actions.
    Uses its intellect (decision-making ability) to achieve favorable circumstances over time.

2. ##States

States define the core actions agents can take, their associated costs, and potential benefits.

    State Modules: Each state is implemented as a separate module, defining its action set and transition logic.
    Action Sets: States provide a set of possible actions (e.g., working, traveling, or taking a break) with their own costs and rewards.
    Transition Costs: Moving from one state to another requires a cost that must be weighed against the expected benefits.
    Agent Intelligence: The "intelligence" of an agent is reflected in its ability to prioritize actions that yield long-term benefits over immediate gains.

Example States:

    Work: Allows agents to earn rewards (e.g., money) at the expense of energy and boredom.
    Travel: Moves agents between locations but incurs costs like time and energy.
    Idle: A fallback state for resting or waiting, with minimal rewards and penalties.

3. ##Genome

The genome represents hereditary information unique to each agent. It encodes genetic traits that influence behavior, decision-making, and performance in various states.
Genes

Genes are the building blocks of an agent's genome, represented as {string, value} pairs. Each gene:

    Impacts the agent’s behavior for specific actions (e.g., Work, Sleep, Eat).
    Modifies state-specific rewards, costs, or performance metrics.

Gene Representation Rules

    Abbreviations: Genes are represented using the first 3–4 characters of their name.
        Example: WorkEfficiency → WorE
    Capitalization Rules:
        If the gene value is positive, the first letter is uppercase: WorE+1.0
        If the gene value is negative, the first letter is lowercase: worE-0.5
    Range Indication: Capitalization of the second character indicates whether the value is within the genomic range.
    Numerical Values: Values are displayed with one decimal point: WorE+1.0

#How It Works
State Transitions

    Action Set Evaluation: Agents evaluate the current state's possible actions using weighted probabilities based on transition costs, state benefits, and genetic predispositions.
    Dynamic Decisions: Decisions are influenced by internal metrics (e.g., energy, boredom), genetic modifiers, and external events.
    Weighted Exit Function: Agents use a probabilistic function to determine if they should exit their current state and which state to transition into.

Agent Performance

The success of an agent is measured by its ability to:

    Balance costs and rewards.
    Adapt behavior based on its genome.
    Optimize well-being over long periods.

Features
1. Modular Design

Each state is a self-contained module with:

    Custom Logic: Unique transition conditions and rewards.
    Dynamic Exit Conditions: Weighted decisions based on agent traits and state metrics.

2. Dynamic Genetics System

The genetic framework introduces variability and individuality in agent behavior:

    Each agent’s genome is randomized at creation.
    Genes influence state performance, transition priorities, and more.

3. Flexible Action Sets

States define action sets, representing possible transitions or behaviors, such as:

    Work → Transition to Travel or Idle.
    Break → Return to Work or enter Idle.

#Planned Features

    Dynamic Environments: Introduce external factors like unexpected events or environmental changes that influence agent behavior.
    Adaptive Learning: Allow agents to modify their genome slightly based on cumulative performance.
    Visualization Tools: Display agent decisions, state transitions, and genome impacts in real time.