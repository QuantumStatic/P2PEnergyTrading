from __future__ import annotations
from Agent import Agent
import random
import CONSTANTS

class Seller(Agent):

    _all_sellers:Seller = []

    def __init__(self, _id:int, init_money:int, energy_generation:int, selling_price:int, load:int, initial_energy:int, max_capacity:int) -> None:
        super().__init__(_id, init_money=init_money, load=load, current_energy=initial_energy, max_capacity=max_capacity)
        Seller._all_sellers.append(self)
        self._setup(energy_generation, selling_price)

    def _setup(self, energy_generation:int, asking_price:int) -> None:
        self._energy_generation = energy_generation
        self._selling_price = asking_price
        self._energy_sold = 0

    @classmethod
    def population(cls) -> int:
        """Returns: Number of sellers in the simulation"""
        return len(cls._all_sellers)

    def generate_energy(self) -> None:
        """Produces energy that it can produce"""
        self._battery.add_charge(self._energy_generation)

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

    @property
    def selling_price(self) -> float:
        """Returns: The energy selling price."""
        return self._selling_price

    @property
    def energy_to_sell(self) -> float:
        """
        Figures out the excessive energy with the seller that it can choose to sell
        Returns: How much energy the seller can sell
        """
        return self._battery.current_capacity - self._load

    def in_price_range(self, price: float) -> bool:
        """
        Returns: True if the price is in the seller's price range, False otherwise
        """
        return ((self._state.modulation_factor-self.tolerance) * self._selling_price) <= price 

    @classmethod
    def any_seller_has_energy(cls) -> bool:
        """Returns: True if there is at least one seller with energy, False otherwise"""
        return any(seller.eligible for seller in cls._all_sellers)

    def __str__(self) -> str:
        return f'Seller {self.__dict__}'

    @classmethod
    def create_sellers(cls, num_sellers:int, init_money, energy_generation:int, asking_price:int, load:int, initial_energy:int) -> list[Seller]:
        """Creates a list of sellers with a given number of sellers"""
        for x in range(num_sellers):
            Seller(x, init_money, energy_generation, asking_price, load, initial_energy, max_capacity=5)
        return cls._all_sellers

    def modulate_selling_price(self) -> None:
        """Modulates the selling price by a random amount with some control"""
        self._selling_price *= random.uniform(0.9, 1.1)
        self._selling_price = max(self._selling_price, CONSTANTS.MIN_ENERGY_PRICE)
        self._selling_price = min(self._selling_price, CONSTANTS.MAX_ENERGY_PRICE)
    
    @property
    def eligible(self) -> bool:
        """Returns: True if the seller is eligible to sell, False otherwise"""
        if self.energy_to_sell > 0:
            return True
        return False

    def approve_for_business(self, agent:Agent, strict:bool=False) -> bool:
        """
        Function check if the recieved is suitable to conduct business with

        Parameters:
        agent: the agent to examine
        strict: when set to true, cause the function to raise an error when type of agent is not suitable for transaction
        """
        if hasattr(agent, 'demand') and hasattr(agent, 'buying_price'):
            return self.in_price_range(agent.buying_price)
        elif strict:
            raise AttributeError("Agent doesn't have a demand or a buyer_price attribute and is trying to aprove for business with a seller")
        return False