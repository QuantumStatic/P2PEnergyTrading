"""
Module that defines multiple states of the agents in the simulation.

Classes:
    Singleton: Implements the singleton design pattern.
    State: Defines the state of the agent.

    other classes that might define states inheriting from state and having singleton as a metaclass
"""
from abc import ABCMeta
import random

class Singleton(type):
    """
    This is a meta class implementing the singleton design pattern.
    """

    _instance = None
    def __call__(cls, *args, **kwargs):
        if cls._instances is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance

class State(metaclass=ABCMeta):
    """
    This is a class used to represent state of an agent. Agent can be normal, desperate, conservative, etc.
    ```
    Attributes
    ----------
    name : str
        The name of the state.
    """

    _multiplier = 1.0

    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def name(self) -> str:
        """
        Returns:
            The name of the state.
        """
        return type(self).__name__

    def __str__(self):
        return self.name

    @property
    def modulation_factor(self) -> float:
        """
        Returns:
            The modulation factor of the state.
        """
        return self._multiplier

    @modulation_factor.setter
    def modulation_factor(self, value: float) -> None:
        """
        Sets the modulation factor of the state.

        Parameters:
            value: The modulation factor of the state.
        """
        self._multiplier = value

class Normal(State):
    """
    This is a class used to represent normal state of an agent.
    """

class Desperate(State):
    """
    This is a class used to represent desperate state of an agent.
    """
    modulation_factor = 0.9

class Conservative(State):
    """
    This is a class used to represent conservative state of an agent.
    """
    modulation_factor = 1.1

def get_state_by_name(name: str) -> State:
    """
    Returns:
        The state with the given name.
    """
    try:
        return eval(name)()
    except NameError:
        raise ValueError(f"No state with name {name}") from NameError

def get_state_randomly() -> State: 
    """
    Returns:
        A random state.
    """
    return random.choice(list(State.__subclasses__()))()