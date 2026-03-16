"""
Implementation of Mesa's meta-agent capability.

Refactored for Mesa 4.0.0 stability, type safety, and predictable state management.
Users should subclass `MetaAgent` to define specific composite behaviors rather 
than relying on dynamic runtime class generation.
"""

from collections.abc import Iterable
from typing import Optional, Type
from mesa import Agent, Model
from mesa.agent import AgentSet


class MetaAgent(Agent):
    """
    A stable, composite Agent that contains other agents.
    
    Subclass this to create specific organizational levels (e.g., City, Corporation, Swarm)
    and define specific `.step()` logic that coordinates the constituting agents.
    """

    def __init__(
        self, 
        model: Model, 
        agents: Optional[Iterable[Agent]] = None, 
        name: str = "MetaAgent"
    ):
        """
        Create a new MetaAgent.

        Args:
            model: The Mesa model instance.
            agents: An optional iterable of agents to include initially.
            name: The name of the MetaAgent.
        """
        super().__init__(model)
        self.name = name
        
        # Initialize an AgentSet to manage the children deterministically
        self._constituting_set = AgentSet(agents or [], random=model.random)

        # Register this meta-agent with its initial children
        for agent in self._constituting_set:
            self._register_child(agent)

    def _register_child(self, agent: Agent) -> None:
        """Safely inject meta-agent tracking onto a child agent."""
        if not hasattr(agent, "meta_agents"):
            agent.meta_agents = set()
        agent.meta_agents.add(self)
        agent.meta_agent = self  # Primary meta-agent pointer

    def _unregister_child(self, agent: Agent) -> None:
        """Safely remove meta-agent tracking from a child agent."""
        if hasattr(agent, "meta_agents"):
            agent.meta_agents.discard(self)
            
            # Safely reassign the primary meta_agent without crashing on mixed unique_id types
            if agent.meta_agents:
                # Extract one deterministically without relying on sortable unique_ids
                agent.meta_agent = next(iter(agent.meta_agents))
            else:
                agent.meta_agent = None

    def add_constituting_agents(self, new_agents: Iterable[Agent]) -> None:
        """Add agents as components."""
        for agent in new_agents:
            self._constituting_set.add(agent)
            self._register_child(agent)

    def remove_constituting_agents(self, remove_agents: Iterable[Agent]) -> None:
        """Remove agents as components."""
        for agent in remove_agents:
            self._constituting_set.discard(agent)
            self._unregister_child(agent)

    @property
    def constituting_agents_by_type(self) -> dict[Type, list[Agent]]:
        """Get the constituting agents grouped by their Python type."""
        grouped = {}
        for agent in self._constituting_set:
            grouped.setdefault(type(agent), []).append(agent)
        return grouped

    @property
    def constituting_agent_types(self) -> set[Type]:
        """Get a set of all unique types of constituting agents."""
        return {type(agent) for agent in self._constituting_set}

    def get_first_constituting_agent_of_type(self, agent_type: Type) -> Agent:
        """
        Get the first instance of a constituting agent of the specified type.
        
        Raises:
            ValueError: If no agent of that type is found.
        """
        agents_of_type = self.constituting_agents_by_type.get(agent_type)
        if not agents_of_type:
            raise ValueError(f"No constituting agent of type {agent_type.__name__} found.")
        return agents_of_type[0]

    # Standard Python magic methods for easy interaction
    def __len__(self) -> int:
        return len(self._constituting_set)

    def __iter__(self):
        return iter(self._constituting_set)

    def __contains__(self, agent: Agent) -> bool:
        return agent in self._constituting_set

    def step(self):
        """
        Perform the agent's step.
        Override this method in subclasses to define the meta-agent's behavior.
        """
        pass