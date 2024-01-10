from __future__ import annotations
from abc import ABC, abstractmethod
from typing import NamedTuple
import random

from Battery import Battery
from State import Normal, get_state_randomly


class Agent(ABC):
    
    BATTERY_LIMIT = 0
    _all_agents:Agent = []

    def __init__(self, _id:int, init_money:int, load:int, current_energy:int, max_capacity:int):
        self._id = _id
        self._INIT_MONEY = init_money
        self._current_money = init_money
        self._load = load
        self._battery = Battery(current_energy, max_capacity)
        self.tolerance = 0.1
        self._state = Normal()
        self._all_agents.append(self)

    @property
    def monery_earned(self) -> int:
        """Returns: The amount of money earned by the agent"""
        return self._current_money - self._INIT_MONEY

    @property
    def money_spent(self) -> int:
        """Returns: The amount of money spent by the agent"""
        return self._INIT_MONEY - self._current_money

    @property
    def _population(self) -> int:
        """Returns: The number of agents in the simulation"""
        return len(Agent._all_agents)

    @property
    def money(self) -> float:
        """Returns: The current money of the agent"""
        return self._current_money

    @property
    def demand(self) -> float:
        """Returns: The demand of the agent"""
        return self._load - self._battery.current_capacity
    
    def consume_energy(self) -> None:
        """Consumes energy from the battery"""
        self._battery.current_capacity -= self._load

    @classmethod
    def set_battery_limit(cls,limit:int) -> None:
        """Sets the battery limit"""
        Agent.BATTERY_LIMIT = limit

    def spend(self, amount:int) -> None:
        """Spends the given amount of money"""
        self._current_money -= amount

    def earn(self, amount:int) -> None:
        """Earns the given amount of money"""
        self._current_money += amount

    @abstractmethod
    def in_price_range(self, price: float) -> bool:
        """Just a placeholder"""

    def modulate_tolerance(self) -> None:
        """Modulates the tolerance of the agent"""
        self.tolerance *= random.uniform(0.9, 1.1)

    @property
    def id(self) -> int:
        """Returns: The id of the agent"""
        return self._id

    @property
    def reserve(self) -> int:
        """Returns: The reserve of the agent"""
        return self._battery.current_capacity

    @property
    def state(self) -> str:
        """Returns: The state of the agent"""
        return self._state.name

    @property
    @abstractmethod
    def eligible(self) -> bool:
        """Returns: True if the agent is eligible to participate in the market, False otherwise"""

    @abstractmethod
    def approve_for_business(self, agent:Agent) -> bool:
        """Returns: True if the agent is approved for business, False otherwise"""

    def reset_state(self) -> None:
        """Resets the state of the agent"""
        self._state = get_state_randomly()

    @staticmethod
    def reset_states(agents:list[Agent]=None) -> None:
        """Resets the states of the given agents"""
        if agents is not None:
            for agent in agents:
                agent.reset_state()
        else:
            for agent in Agent._all_agents:
                agent.reset_state()

    @staticmethod
    def check_match_for_business(agent1:Agent, agent2:Agent) -> bool:
        """
        Function that checks compatibility of 2 agents to make a transaction

        Parameters:
        agent1: first agent to be checked for compatibility 
        agent2: second agent to be checked for compatibilty

        Returns:
        None if transaction is not possible
        A Named Tuple if transaction is possible having the amount of energy to be exchanged and the rate of energy
        """
        if agent1.approve_for_business(agent2) and agent2.approve_for_business(agent1):
            if agent1.demand > 0:
                transaction_energy = min(agent1.demand, agent2.energy_to_sell, agent1.money // agent2.selling_price)
                selling_price = agent2.selling_price
            else:
                transaction_energy = min(agent2.demand, agent1.energy_to_sell, agent2.money // agent1.selling_price)
                selling_price = agent1.selling_price
            
            Link_details = NamedTuple('link_details', [('energy', int), ('price', int)])
            return Link_details(energy=transaction_energy, price=selling_price)

    def do_business_with_details(self, price:float, energy:float) -> None:
        """
        Function that executes the transaction between 2 agents

        Parameters:
        agent: The agent with which the transaction is to be executed
        """
        pass

    @staticmethod
    def do_business(agent1:Agent, agent2:Agent, energy:float, price:float) -> tuple[Agent]:
        fin_ret = None
        fin_ret:tuple[Agent] = (agent1, agent2) if agent1.demand > 0 else (agent2, agent1)
            
        agent1.do_business_with_details(price, energy)
        agent2.do_business_with_details(price, energy)

        return fin_ret