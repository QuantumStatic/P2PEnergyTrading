from Grid import Grid

class Battery:

    def __init__(self, current_capacity: int, max_capacity: int):
        self._max_capacity = max_capacity
        self._current_capacity = current_capacity

    def add_charge(self, charge_to_add: int) -> None:
        if self._current_capacity + charge_to_add > self._max_capacity:
            Grid()(self._current_capacity + charge_to_add - self._max_capacity)
            self._current_capacity = self._max_capacity
        else:
            self._current_capacity += charge_to_add
    
    def remove_charge(self, charge_to_remove: int) -> None:
        if self._current_capacity - charge_to_remove < 0:
            self._current_capacity = 0
        else:
            self._current_capacity -= charge_to_remove
    
    @property
    def current_capacity(self) -> int:
        return self._current_capacity

    @current_capacity.setter
    def current_capacity(self, new_capacity: int) -> None:
        self._current_capacity = new_capacity

    @property
    def max_capacity(self) -> int:
        return self._max_capacity