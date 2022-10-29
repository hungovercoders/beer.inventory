from enum import Enum
from typing import Union, List
from fastapi import FastAPI, status, Response, Body
from pydantic import BaseModel, Field

class Flavour(str, Enum):
    """_summary_

    Args:
        str (_type_): _description_
        Enum (_type_): _description_
    """
    HOPPY = "Hoppy"
    CHOCOLATE = "Chocolate"
    CARAMEL = "Caramel"
    ORANGE = "Orange"
    
class Beer(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    name: str = Field(example="Mike Rayer")
    brewer: str = Field(example="Crafty Devil")
    strength: float = Field(example=5.2)
    flavours: Union[List[Flavour], None] = Field(default=None
                                                 ,example=["Caramel"])
    
    def __getitem__(self, item):
        return getattr(self, item)
    
 
beer_list = []
beer1 = Beer(name="Mike Rayer",brewer="Crafty Devil",strength=4.6, flavours=["Caramel"])
beer_list.append(beer1)

beerapi = FastAPI()

@beerapi.post("/beers/")
async def create_beer(response: Response, beer: Beer= Body(
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Elvis Juice",
                    "brewer": "Brewdog",
                    "strength": 4.6,
                    "flavours": ["Orange"],
                },
            },
            "invalidMissingStrength": {
                "summary": "Beers without a strength are rejected",
                "value": {
                    "name": "Mike Rayer",
                    "brewer": "Crafty Devil"
                },
            },
        },
    )):
    """_summary_

    Args:
        beer (Beer): _description_

    Returns:
        _type_: _description_
    """
    if beer not in beer_list:
        beer_list.append(beer)
        content = f'Beer "{beer.name}" Added.'
        response.status_code=status.HTTP_201_CREATED
    else:
        content = f'Beer "{beer.name}" Already Exists.'
    return content

@beerapi.get("/beers/")
async def get_beers():
    """_summary_

    Returns:
        _type_: _description_
    """

    return beer_list

@beerapi.get("/beers/{name}/")
async def get_beer(name: str):
    """_summary_

    Returns:
        _type_: _description_
    """
    try:
        beer = [beer for beer in beer_list if beer.name.replace(' ','').lower() 
                == name.replace(' ','').lower()][0]
    except IndexError:
        return f'Beer "{name}" does not exist.'
    return beer

@beerapi.delete("/beers/{name}/")
async def delete_beer(name: str):
    """_summary_

    Returns:
        _type_: _description_
    """

    try:
        beer = [beer for beer in beer_list if beer.name.replace(' ','').lower() 
                == name.replace(' ','').lower()][0]
    except IndexError:
        return f'Beer "{name}" does not exist.'

    for idx, item in enumerate(beer_list):
        if beer["name"] in item["name"]:
            beer_index = idx

    if beer in beer_list:
        del beer_list[beer_index]
        return f'Beer "{name}" removed.'
