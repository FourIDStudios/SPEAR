# Agent-Based AI System

## Overview

This project explores the development of an **agent-based artificial intelligence system** designed to simulate agents interacting with their environment. These agents will perceive their surroundings, make decisions based on those perceptions, and adapt over time. The system will evolve from simple rule-based models to more sophisticated decision-making frameworks, such as utility-based AI, reinforcement learning (RL), and potentially genetic algorithms (GAs).

## Table of Contents
- [Goals](#goals)
- [Key Milestones](#key-milestones)
- [Current Development Path](#current-development-path)
- [Features](#features)
- [Planned Features](#planned-features)
- [Getting Started](#getting-started)

## Case Study: Identifying Key Factors Affecting AI Decision-Making

The ultimate goal of this project is to serve as a **case study** for identifying and understanding the **significant factors** that influence artificial intelligence decision-making. Through this exploration, we aim to uncover which variables and approaches most effectively impact the behavior of intelligent agents in complex environments.

### Approach

Our approach is unique in that it evolves into an amalgamation of varied ai systems, our system will maintain a state based approach as to allow visualizing and understanding "the flow" of an Agent to be simplier, without loosing out on the complexities involved in complex nural networks, 
this wil also allow us to configure variouse aspects of the Agent that wouldn't otherwise be possible with a more singular system. I understand that this isn't anything 'revolutionary' but i think exploring the small nuances that affect an Agents decision making is worthwhile, similar to how
we utilized the Sigmoid function to calculate relative weights until we realized that the much simplier ReLU approach resulted in 'faster learners'. In simplier terms, sometimes simplicity is key.

By gradually introducing advanced AI systems like **utility-based models**, **reinforcement learning**, and **genetic algorithms**, we aim to test and identify which techniques provide the most robust and effective solutions for managing the complexity of state transitions in real-time.

Ultimately, the goal is to develop a system that can:
- Combine the strengths of traditional AI and neural-based learning models.
- Handle complex and dynamic state transitions through an evolving, adaptable decision-making process.
- Improve over time, learning from experiences and adjusting to new challenges in the environment.

This case study will contribute to understanding the evolution of agent-based AI and provide insights into how various learning mechanisms can be integrated into a unified system for complex decision-making. You can find more clearly defined goals below.

## Goals

The primary goal is to create agents that can:

- **Perceive**: Gather information from their environment.
- **Decide**: Make decisions based on their perceptions and internal needs.
- **Adapt**: Learn from their experiences and improve over time.

The system follows a standard AI pipeline:
- **Input** (Perception) → **Processing** (Decision-Making) → **Output** (Actions) → **Feedback** (Learning)

## Key Milestones

1. **Basic Rule-Based Agent**: An agent that transitions between predefined states with simple decision-making rules.
2. **Utility-Based Agent**: Agents choose actions based on the value of each potential outcome.
3. **Reinforcement Learning Agent**: Q-Learning or Deep Q-Learning trained agents to enable longer-term optimization and learning.
4. **Genetic Algorithms (Optional)**: Evolving agents that improve over multiple generations, simulating human-like learning.

## Current Development Path

### Step 1: Foundation of the Agent System
We begin by defining the core components of the agent:

#### Agent Object
- **Attributes**: Hunger, energy, social needs, and other variables that influence the agent’s actions.
- **Genome**: Encodes genetic information that affects decision-making and agent behavior.
- **State Management**: Tracks the agent’s current state and potential actions to transition between states.
- **Perception**: A system to observe changes in the environment (e.g., detecting hunger or nearby threats).
- **Decision-Making**: Logic that allows the agent to choose the most appropriate action based on its current needs and environment.

#### Environment
Defines the world the agent operates in, including:
- **Resources**, **threats**, or **interactions with other agents**.
- Can be grid-based, event-driven, or dynamically generated based on certain conditions.

### Step 2: Implementing Simple AI

We will start by creating simple AI models:

#### Rule-Based AI
- The agent follows basic predefined rules (e.g., “if hunger is high, move to eat”).
- Simple state transitions without the ability to adapt or plan ahead.

#### Utility-Based AI
- Actions are evaluated based on the agent's internal needs (e.g., energy, hunger, or safety).
- The agent will execute the highest-value action according to its current state.
- Introduces a basic form of decision-making based on priorities.

### Step 3: Learning Mechanisms

Once basic AI is functional, we will move to learning systems:

#### Reinforcement Learning (RL)
- Train agents using a reward-punishment system to reinforce positive behaviors and discourage negative ones.
- Use Q-Learning or basic RL algorithms where agents learn to associate actions with rewards or penalties.
- Example: Reward eating when hungry, penalize starvation.

#### Deep Reinforcement Learning (Optional)
- Once basic RL setup is successful, extend it to deep RL, where agents use neural networks to learn and adapt in more complex environments.

### Step 4: Genetic Algorithms (Stretch Goal)

If time and resources allow, genetic algorithms (GAs) will be explored as an advanced method of evolving agents:

#### Genetic Algorithms
- Evolving agents over multiple generations.
- Agents “mate” based on fitness, and mutations introduce diversity into the population.
- Aims to simulate a more biological form of learning, offering long-term adaptation strategies.

## Features

- **Modular Agent Design**: Independent modules for states, actions, and decision-making, allowing for easy swaps as agent intelligence increases.
- **Dynamic State Management**: Agents evaluate and transition between states based on their internal needs and environment. Transition logic changes as more advanced AI systems (utility-based, RL) are introduced.
- **Adaptive Learning**: The system will include feedback mechanisms to allow agents to learn from experiences, considering both short-term rewards and long-term optimization goals.
- **Flexible Genome System**: Genetic traits influence agent decision-making and behavior. Potential for evolving agents over time with GAs.

## Planned Features

- **Reinforcement Learning**: Gradually introduce RL techniques to improve agent behavior over time.
- **Deep Q-Learning**: Implement deep reinforcement learning for more complex decision-making.
- **Visualization Tools**: Real-time visualization of agent behavior, decision-making, and adaptation.
- **Adaptive Environments**: Integrate dynamic environmental changes or random events to challenge agents and test adaptability.

## Getting Started

To get started with the project:
    TBD

## Contributing

We welcome contributions to this project. To contribute: (TBD This is not the final format)

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
