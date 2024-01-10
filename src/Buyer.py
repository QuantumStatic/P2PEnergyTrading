"""
This python file has an example python class for the functionality of buying
"""

from __future__ import annotations
import random
from Agent import Agent
import CONSTANTS


class Buyer(Agent):

    _all_buyers:Buyer = []

    def __init__(self, _id:int, init_money:int, buying_price:int, load:int, initial_energy:int, max_capacity:int) -> None:
        super().__init__(_id, init_money, load, initial_energy, max_capacity)
        Buyer._all_buyers.append(self)
        self._setup(buying_price)

    def _setup(self, buying_price:int) -> None:
        self._buying_price = buying_price
        self._energy_bought = 0

    @classmethod
    def population(cls) -> int:
        """Returns: the number of buyers in the simulation"""
        return len(cls._all_buyers)

    @property
    def energy_to_buy(self) -> int:
        """Returns: the amount of energy the buyer needs to buy"""
        return self._load - self._battery.current_capacity

    def buy_energy(self, bought_energy:int, price:int) -> None:
        """
        buys the given amount of energy for the specified price

        Parameters:
            bought_energy: the amount of energy to be bought
            price: price of the energy
        """
        self._energy_bought += bought_energy 
        self._battery.add_charge(bought_energy)
        self.spend(price)

    def in_price_range(self, price: float) -> bool:
        return price*self._state.modulation_factor <= ((1+self.tolerance) * self._buying_price)

    def modulate_buying_price(self) -> None:
        """Modulates the buying price of the buyer"""
        self._buying_price *= random.uniform(0.9, 1.1)
        self._buying_price = max(self._buying_price, CONSTANTS.MIN_ENERGY_PRICE)
        self._buying_price = min(self._buying_price, CONSTANTS.MAX_ENERGY_PRICE)

    @property
    def buying_price(self):
        """Returns: the buying price of the buyer."""
        return self._buying_price

    @classmethod
    def is_available(cls) -> bool:
        """Returns: True if there is at least one buyer in the simulation, False otherwise"""
        return any(buyer.eligible for buyer in cls._all_buyers)

    @classmethod
    def create_buyers(cls, init_money:int,num_buyers:int, buying_price:int, load:int, initial_energy:int) -> list:
        for x in range(num_buyers):
            Buyer(_id=x, buying_price=buying_price, load=load, initial_energy=initial_energy, init_money=init_money, max_capacity=5)
        return cls._all_buyers

    @property
    def eligible(self) -> bool:
        """Returns: True if the buyer is eligible to buy, False otherwise"""
        if self.money > 0 and self.energy_to_buy > 0:
            return True
        return False

    def approve_for_business(self, agent:Agent, verbose:bool = False) -> bool:
        """
        Function check if the recieved is suitable to conduct business with

        Parameters:
        agent: the agent to examine
        strict: when set to true, cause the function to raise an error when type of agent is not suitable for transaction
        """
        if hasattr(agent, 'energy_to_sell') and hasattr(agent, 'selling_price') and agent.selling_price is not None:
            return self.in_price_range(agent.selling_price)
        elif verbose:
                raise AttributeError("Agent does not have either elling_price or energy_to_sell attribute and is trying to aprove for business with a buyer")
        return False

    def do_business_with_details(self, price:float, energy:float) -> None:
        self.buy_energy(energy, price)
        self.modulate_buying_price()
        self.modulate_tolerance()
        