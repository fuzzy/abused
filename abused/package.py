""" abused.package  """

# Stdlib imports
from typing import List


class Package:

    _name: str
    _category: str
    _version: str
    _variables: dict

    def __init__(self, atom: str) -> None:
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
