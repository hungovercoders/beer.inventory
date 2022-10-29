from enum import Enum

from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Beer(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    name: str
    brewer: str
    strength: float
    flavours: Union[list, None] = None
    
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