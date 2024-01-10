class Grid:
    _instance = None

    def __new__(self):
        if self._instance is None:
            self._instance = super().__new__(self)
        return self._instance

    def __init__(self):
        self._drained_energy = 0

    def __call__(self, energy_to_drain: int):
        self._drained_energy += energy_to_drain

    def get_drained_energy(self) -> int:
        return self._drained_energy
