from enum import Enum
from typing import Union, List
from fastapi import FastAPI
from pydantic import BaseModel

class Flavour(str, Enum):
    """_summary_

    Args:
        str (_type_): _description_
        Enum (_type_): _description_
    """
    HOPPY = "Hoppy"
    CHOCOLATE = "Chocolate"
    CARAMEL = "Caramel"


class Beer(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    name: str
    brewer: str
    strength: float
    flavours: Union[List[Flavour], None] = None

beerapi = FastAPI()

@beerapi.post("/beers/")
async def create_item(beer: Beer):
    """_summary_

    Args:
        beer (Beer): _description_

    Returns:
        _type_: _description_
    """
    return beer
