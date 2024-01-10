"""
This file defines an example of a class that implements a mixed functionality of buying and selling
"""

import random
from Agent import Agent
import CONSTANTS

from typing import Union

class Prosumer(Agent):

    """
    This is a seperate class because dimaond inheritance wasn't possible.
    """

    _all_prosumers = []

    def __init__(self, _id:int, init_money:int, energy_generation:int, selling_price:int, load:int, initial_energy:int, max_capacity:int, buying_price:int):
        super().__init__(_id, init_money=init_money, load=load, current_energy=initial_energy, max_capacity=max_capacity)
        Prosumer._all_prosumers.append(self)
        self._setup(energy_generation, selling_price, buying_price)

    def _setup(self, energy_generation:int, asking_price:int, buying_price:int) -> None:
        """
        Breaking init down to seperate function
        """
        self._energy_generation = energy_generation
        self._selling_price = asking_price
        self._energy_sold = 0
        self._buying_price = buying_price
        self._energy_bought = 0
        self._mode: bool = False # False for buying, True for selling, None for neither

    @classmethod
    def population(cls) -> int:
        """Returns: the number of prosumers in the simulation"""
        return len(cls._all_prosumers)

    @property
    def energy_to_buy(self) -> int:
        """Returns: the amount of energy the prosumer needs to buy"""
        if self._mode is False:
            return max(self._load - self._battery.current_capacity, 0)

    @property
    def energy_to_sell(self) -> float:
        """
        Figures out the excessive energy with the seller that it can choose to sell
        Returns: How much energy the seller can sell
        """
        if self._mode is True:
            return max(self._battery.current_capacity - self._load, 0)

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

    def sell_energy(self, energy_sold:int, price:int) -> None:
        """
        Sell a given amount of energy at a given price.

        Parameters:
            energy_sold: How much energy to sell
            price: At what price energy to sell
        """
        self._energy_sold += energy_sold
        self._battery.current_capacity -= energy_sold
        self.earn(price)

    def in_buying_range(self, price: float) -> bool:
        """
        Returns: True if the price is in the buyers's price range, False otherwise
        """
        return price*self._state.modulation_factor <= ((1+self.tolerance) * self._buying_price)
    
    def in_selling_range(self, price: float) -> bool:
        """
        Returns: True if the price is in the seller's price range, False otherwise
        """
        return ((self._state.modulation_factor-self.tolerance) * self._selling_price) <= price

    def in_price_range(self, price: float) -> bool:
        """
        Returns: True if the price is in the seller's price range, False otherwise
        """
        if self._mode is True:
            return self.in_selling_range(price)
        elif self._mode is False:
            return self.in_buying_range(price)
        return False

    def modulate_buying_price(self) -> None:
        """Modulates the buying price of the buyer""" 
        self._buying_price *= random.uniform(0.9, 1.1)
        self._buying_price = max(self._buying_price, CONSTANTS.MIN_ENERGY_PRICE)
        self._buying_price = min(self._buying_price, CONSTANTS.MAX_ENERGY_PRICE)

    def modulate_selling_price(self) -> None:
        """Modulates the selling price by a random amount with some control"""
        self._selling_price *= random.uniform(0.9, 1.1)
        self._selling_price = max(self._selling_price, CONSTANTS.MIN_ENERGY_PRICE)
        self._selling_price = min(self._selling_price, CONSTANTS.MAX_ENERGY_PRICE)

    @property
    def buying_price(self) -> Union[float, None]:
        """Returns: the buying price of the buyer."""
        if self._mode is False:
            return self._buying_price

    @property
    def selling_price(self) -> Union[float, None]:
        """Returns: The energy selling price."""
        if self._mode is True:
            return self._selling_price

    @classmethod
    def is_available(cls) -> bool:
        """Returns: True if there is at least one buyer in the simulation, False otherwise"""
        return any(prosumer.eligible for prosumer in cls._all_prosumers) 

    def _set_mode(self) -> bool:
        """ Sets the mode of the prosumer."""
        net_energy = self._load - self._battery.current_capacity
        self._mode = (net_energy < 0)
        return self._mode

    @property
    def eligible(self) -> bool:
        """
        Check eligibilty of the prosumer object to participate in the market
        """
        mode = self._set_mode()
        if mode is True:
            return self._eligible_for_selling()
        if mode is False:
            return self._eligible_for_buying()
        
        return False

    def _eligible_for_buying(self) -> bool:
        """Returns: True if the buyer is eligible to buy, False otherwise"""
        if self.money > 0 and self.energy_to_buy > 0:
            return True

        return None

    def _eligible_for_selling(self) -> bool:
        """ Checks is prosumer is eligible to sell """
        if self.energy_to_sell > 0:
            return True
        return False
    
    def approve_for_business(self, agent: Agent, strict:bool = False) -> bool:
        """Checks if the passed agant is aproved for business
        returns: True is aproved for business and false if not aprooved for business
        """
        if self._mode is True:
            return self._aprove_for_selling_to(agent, strict)
        if self._mode is False:
            return self._aprove_for_buying_from(agent, strict)
        return False

    def _aprove_for_buying_from(self, agent:Agent, strict:bool) -> bool:
        """
        Internal function to check if the passed agent is suitable to buy from
        """
        if hasattr(agent, 'energy_to_sell') and hasattr(agent, 'selling_price') and agent.energy_to_sell is not None:
            return self.in_buying_range(agent.selling_price)
        elif strict:
            raise AttributeError("Agent does not have energy_to_sell or selling_price attribute and is trying to aprove for business with a buyer")
        else:
            return False

    def _aprove_for_selling_to(self, agent:Agent, strict:bool) -> bool:
        """
        Internal function to check if the passed agent is suitable to sell to
        """
        if hasattr(agent, 'demand') and hasattr(agent, 'buying_price') and agent.demand > 0:
            return self.in_selling_range(agent.buying_price)
        if strict:
            raise AttributeError("Agent doesn't have a demand or buying_price and is trying to aprove for business with a seller")
        return False

    def generate_energy(self) -> None:
        """Produces energy that it can produce"""
        self._battery.add_charge(self._energy_generation)

    def do_business_with_details(self, price:float, energy:float) -> None:
        """Does business with the given price and energy"""
        if self._mode is True:
            self.sell_energy(energy, price)
            self.modulate_selling_price()
        elif self._mode is False:
            self.buy_energy(energy, price)
            self.modulate_buying_price()
        
        self.modulate_tolerance()