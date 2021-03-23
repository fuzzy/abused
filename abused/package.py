""" abused.package  """

# Stdlib imports
from typing import List


class Package:

    _name: str
    _category: str
    _version: str
    _variables: dict
    _line: str
    _flattened: List[str]

    def __init__(self, atom: str) -> None:
        self.category = atom.strip().split("/")[0]
        pass

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def category(self) -> str:
        return self._category

    @category.setter
    def category(self, value: str) -> None:
        self._category = value

    @property
    def version(self) -> str:
        return self._version

    @property
    def variables(self) -> dict:
        return self._variables

    @variables.setter
    def variables(self, key: str, value: List[str]) -> None:
        self._variables[key] = value

    @property
    def line(self) -> str:
        return self._line

    @line.setter
    def line(self, value: str) -> None:
        self._line = value

    @property
    def flattened(self) -> List[str]:
        return self._flattened

    @flattened.setter
    def flattened(self, data: List[str]) -> None:
        self._flattened = data
