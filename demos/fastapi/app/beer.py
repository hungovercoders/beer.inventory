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
    strength: float = Field(gt=0,lt=100,example=5.2
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
        UserList: Inherited from collections
    """

    def __init__(self, iterable):
        """Starts a collection of an iterable object

        Args:
            iterable (_type_): An object that can be iterated over_
        """
        super().__init__(self._validate_beer(item) for item in iterable)

    def append(self, item):
        """Adds a beer item

        Args:
            item (_type_): A beer object

        Returns:
            boolean: Whether item was added or not
        """
        if item not in self:
            self.data.append(self._validate_beer(item))
            return True
        return False

    def remove(self, item):
        """Removes a beer

        Args:
            item (_type_): A beer object

        Returns:
            boolean: Whether item was removed or not
        """
        if item in self:
            self.data.remove(self._validate_beer(item))
            return True
        return False

    def _validate_beer(self, value):
        """Validates item is a Beer object

        Args:
            value (_type_): Object to be validated

        Raises:
            TypeError: Errors if object is not beer

        Returns:
            Beer: Beer object if valid 
        """
        if isinstance(value, (Beer)):
            return value
        raise TypeError(
            f"beer object expected, got {type(value).__name__}")

    def get_beer_by_name(self, name) -> Optional[Beer]:
        """Gets beer from list by name

        Args:
            name (string): The name of the beer

        Returns:
            Optional[Beer]: The beer that matches the beer name
        """
        beer = None
        try:
            beer = [beer for beer in self if beer.name.replace(' ','').lower()
                == name.replace(' ','').lower()][0]
        except IndexError:
            print (f'Beer "{name}" does not exist.')
        return beer

    def get_beer_index_by_name(self, name) -> Optional[int]:
        """Gets beer index in the list by its name

        Args:
            name (string): The name of the beer

        Returns:
            Optional[int]: The index position of the beer in the list
        """
        beer_index = None
        beer = self.get_beer_by_name(name)
        if beer is not None:
            for idx, item in enumerate(self):
                if beer["name"] in item["name"]:
                    beer_index = idx
        return beer_index

    def set_beer_by_name(self, name, beer):
        """Updates the beer in the list by its name

        Args:
            name (string): The name of the beer
            beer (Beer): The Beer object to be updated to
        """
        if beer.name != name:
            error = "You cannot alter the name of a beer as this is the unique identifier."
            raise ValueError(error)
        index = self.get_beer_index_by_name(name)
        if index is not None:
            super().__setitem__(index, beer)
            return True
        self.append(beer)
        return False

    def remove_beer_by_name(self, name):
        """Removes the beer from the list by its name

        Args:
            name (string): The name of the beer
        """
        beer = self.get_beer_by_name(name)
        if beer is not None:
            return self.remove(beer)
        return True
