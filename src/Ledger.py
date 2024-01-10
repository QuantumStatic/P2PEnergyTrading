"""
This file contains code to maintain a ledger.
"""

from typing import Union
from excel_readwrite import write_data_to_excel

class Ledger:
    """
    Class ledger representing ledger
    """

    def __init__(self, path:str, headers: Union[list[str], tuple[str]]) -> None:
        self._path = path
        self._enteries = 0
        write_data_to_excel(self._path, headers)

    def add_entry(self, entry: Union[dict[str, list], list, tuple]) -> None:
        """
        Functions appends to the currently in use excel file

        Paramters:
        entry: Data to add
        """
        write_data_to_excel(self._path, entry)
        self._enteries += 1

    @property
    def enteries(self) -> int:
        return self._enteries