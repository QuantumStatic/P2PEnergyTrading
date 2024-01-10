"""
This file contains code to simulate the market for energy interchange. 
"""

from __future__ import annotations
from typing import NamedTuple, Union, Iterable

import CONSTANTS
from Ledger import Ledger

from Agent import Agent

class Market:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, max_price: int, min_price: int) -> None:
        self._energy_price = 0
        self._ledger = Ledger(CONSTANTS.LEDGER_FILE_PATH, [
            "Round", "Buyer ID", "Seller ID", "Energy", "Price", "Money/Energy", "agent1 reserve", "agent2 reserve"])
        self.set_energy_prices(max_price, min_price)

    def set_energy_prices(self, max_price: int, min_price: int) -> None:
        CONSTANTS.MAX_ENERGY_PRICE = max_price
        CONSTANTS.MIN_ENERGY_PRICE = min_price

    @staticmethod
    def filter_eligible(agents:list[Agent]) -> Iterable[Agent]:
        """
        Takes in a list of agents and returns only eligible agents
        """
        return filter(lambda agent: agent.eligible, agents)

    def do_they_match(self, agent1: Agent, agent2: Agent) -> Union[tuple[int, int], None]:
        """
        
        """
        return Agent.check_match_for_business(agent1, agent2)

    def do_commerce(self, agent1: Agent, agent2: Agent, energy: int, price: int, market_round:int = 1) -> None:
        """
        Transaction between a selling entity and a buying entity happens in this function

        Parameters:
        agent1: An agent that's taking part in the transaction
        agent2: Another agent taking part in the transaction 
        energy: measure of energy being exchanged in the transaction
        price: price at which energy is being sold
        market_round: currently which market round we are on
        """
        (agent1, agent2) = Agent.do_business(agent1, agent2, energy, price)
        
        self._ledger.add_entry(
            [market_round,  agent2.id, agent1.id, energy, price, price/energy,  agent2.reserve, agent1.reserve])

    def ideal_fair_market(self, buyers: list[Agent], sellers: list[Agent]) -> None:
        """
        This function simulates a ideal market. Both the contenders are restricted to 1 transaction per round.

        Parameters:
        buyers: takes a list of buyers or any other Agent extended class that has the ability to buy
        sellers: takes a list of sellers or nay other Agent extended class that has the ability to sell
        """

        for agent2 in sellers:
            agent2.generate_energy()

        market_round = 1
        all_agents = buyers + sellers

        while market_round < CONSTANTS.MAX_MARKET_ROUNDS:
            all_agents_cpy, buyer_idx = list(Market.filter_eligible(all_agents)), 0
            # count = 0
            while buyer_idx < len(all_agents_cpy):
                if not all_agents_cpy[buyer_idx].eligible:
                    buyer_idx += 1
                    continue
                # print(count, buyer_idx)
                # count += 1

                seller_idx = buyer_idx + 1
                while seller_idx < len(all_agents_cpy):
                    if (link_details := self.do_they_match(all_agents_cpy[buyer_idx], all_agents_cpy[seller_idx])) is not None:
                        self.do_commerce(all_agents_cpy[buyer_idx], all_agents_cpy[seller_idx], link_details.energy, link_details.price)

                        break

                    seller_idx += 1
                else:
                    buyer_idx += 1

            market_round += 1
            Agent.reset_states(buyers)
            Agent.reset_states(sellers)
            print(market_round)

    def real_world_market(self, buyers: list[Agent], sellers: list[Agent]) -> None:
        """
        This function simulates a real world market. Both the contenders are not restricted to 1 transaction per round.

        Parameters:
        buyers: takes a list of buyers or any other Agent extended class that has the ability to buy
        sellers: takes a list of sellers or nay other Agent extended class that has the ability to sell
        """
        for agent2 in sellers:
            agent2.generate_energy()

        market_round = 1
        all_agents = buyers + sellers

        while market_round < CONSTANTS.MAX_MARKET_ROUNDS:
            all_agents_cpy, buyer_idx = list(Market.filter_eligible(all_agents)), 0
            # count = 0
            while buyer_idx < len(all_agents_cpy):
                if not all_agents_cpy[buyer_idx].eligible:
                    buyer_idx += 1
                    continue
                # print(count, buyer_idx)
                # count += 1

                seller_idx = buyer_idx + 1
                while seller_idx < len(all_agents_cpy):
                    if (link_details := self.do_they_match(all_agents_cpy[buyer_idx], all_agents_cpy[seller_idx])) is not None:
                        self.do_commerce(all_agents_cpy[buyer_idx], all_agents_cpy[seller_idx], link_details.energy, link_details.price, market_round)

                        (lower_idx, higher_idx) = (seller_idx, buyer_idx) if buyer_idx > seller_idx else (buyer_idx, seller_idx)

                        for idx in (higher_idx, lower_idx):
                            participant = all_agents_cpy.pop(idx)
                            if participant.eligible:
                                # Buyer/Seller is shifted to the end of line if it is still eligible 
                                all_agents_cpy.append(participant)

                        break

                    seller_idx += 1
                else:
                    buyer_idx += 1

            market_round += 1
            Agent.reset_states(buyers)
            Agent.reset_states(sellers)
            
            for agent in all_agents:
                try:
                    agent.generate_energy()
                finally:
                    agent.consume_energy()
            
            print(market_round)


