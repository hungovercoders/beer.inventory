from enum import Enum
from typing import Union, List, Optional
from pydantic import BaseModel, Field
from collections import UserList

class Flavour(str, Enum):
    """This is a flavour of a beer

    Args:
        str (_type_): _description_
        Enum (_type_): _description_
    """
    HOPPY = "Hoppy"
    CHOCOLATE = "Chocolate"
    CARAMEL = "Caramel"
    ORANGE = "Orange"

class Beer(BaseModel):
    """This is a beer

    Args:
        BaseModel (_type_): _description_
    """
    name: str = Field(example="Mike Rayer"
                      ,description="This is the name of the beer")
    brewer: str = Field(example="Crafty Devil"
                        ,description="This is the name of the brewer of the beer")
    strength: float = Field(example=5.2
                            ,description="This is the strength of the alcohol in the beer")
    flavours: Union[List[Flavour], None] = Field(default=None
                                                 ,example=["Caramel"]
                                                 ,description="These are the lists \
                                                 of flavours in the beer")

    def __getitem__(self, item):
        return getattr(self, item)

class BeerList(UserList):
    """This is a beer list. Acting as an in-memory data store for demos.

    Args:
        UserList: _description_
    """

    def __init__(self, iterable):
        """_summary_

        Args:
            iterable (_type_): _description_
        """
        super().__init__(self._validate_beer(item) for item in iterable)

    def append(self, item):
        """_summary_

        Args:
            item (_type_): _description_

        Returns:
            _type_: _description_
        """
        if item not in self:
            self.data.append(self._validate_beer(item))
            return True
        return False

    def remove(self, item):
        """_summary_

        Args:
            item (_type_): _description_

        Returns:
            _type_: _description_
        """
        if item in self:
            self.data.remove(self._validate_beer(item))
            return True
        return False

    def _validate_beer(self, value):
        """_summary_

        Args:
            value (_type_): _description_

        Raises:
            TypeError: _description_

        Returns:
            _type_: _description_
        """
        if isinstance(value, (Beer)):
            return value
        raise TypeError(
            f"beer object expected, got {type(value).__name__}")

    def get_beer_by_name(self, name) -> Optional[Beer]:
        """_summary_

        Args:
            name (_type_): _description_

        Returns:
            Optional[Beer]: _description_
        """
        beer = None
        try:
            beer = [beer for beer in self if beer.name.replace(' ','').lower()
                == name.replace(' ','').lower()][0]
        except IndexError:
            print (f'Beer "{name}" does not exist.')
        return beer

    def get_beer_index_by_name(self, name) -> Optional[int]:
        """_summary_

        Args:
            name (_type_): _description_

        Returns:
            Optional[int]: _description_
        """
        beer = self.get_beer_by_name(name)
        if beer is not None:
            beer_index = None
            for idx, item in enumerate(self):
                if beer["name"] in item["name"]:
                    beer_index = idx
            return beer_index

    def set_beer_by_name(self, name, beer):
        """_summary_

        Args:
            name (_type_): _description_
            beer (_type_): _description_
        """
        if beer.name != name:
            raise ValueError("You cannot alter the name of a beer as \
                             this is the unique identifier.")
        index = self.get_beer_index_by_name(name)
        if index is not None:
            super().__setitem__(index, beer)
            return True
        self.append(beer)

    def remove_beer_by_name(self, name):
        """_summary_

        Args:
            name (_type_): _description_
        """
        beer = self.get_beer_by_name(name)
        if beer is not None:
            return self.remove(beer)
