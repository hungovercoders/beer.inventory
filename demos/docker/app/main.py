from fastapi import FastAPI, status, Response, Body
from pydantic import BaseModel, Field
from typing import Union, List
from enum import Enum

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

beer_list = []
beer1 = Beer(name="Mike Rayer",brewer="Crafty Devil",strength=4.6)
beer_list.append(beer1)
beer2 = Beer(name="Stay Puft",brewer="Tiny Rebel",strength=4.8)
beer_list.append(beer2)

app = FastAPI()

@app.get("/")
async def root():
    """Welcomes you to the beer API

    Returns:
        string: Welcome message
    """
    return "Welcome to the beer API!"

@app.get("/beers/")
async def get_beers(response: Response):
    """Returns all available beers

    Returns:
        list[Beer]: Returns a list of beer objects
    """
    response.status_code=status.HTTP_200_OK
    return beer_list

@app.post("/beers/")
async def create_beer(response: Response, beer: Beer= Body(
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Elvis Juice",
                    "brewer": "Brewdog",
                    "strength": 4.6
                },
            },
             "beerTooStrong": {
                "summary": "Too strong beer fails",
                "description": "This is a beer with a strength above 100%.",
                "value": {
                    "name": "Elvis Juice",
                    "brewer": "Brewdog",
                    "strength": 101.0
                },
            },
            "beerTooWeak": {
                "summary": "Too weak beer fails",
                "description": "This is a beer with a strength below 0%.",
                "value": {
                    "name": "Elvis Juice",
                    "brewer": "Brewdog",
                    "strength": -1.0
                },
            },
            "invalidMissingStrength": {
                "summary": "Beers without a strength are rejected",
                "description": "Beers without a strength are rejected",
                "value": {
                    "name": "Mike Rayer",
                    "brewer": "Crafty Devil"
                },
            },
            "beerGoodFlavour": {
                "summary": "Good flavour addition",
                "description": "This is a beer with an allowable list of flavours",
                "value": {
                    "name": "Old Abbot",
                    "brewer": "Hogwarts",
                    "strength": 5.0,
                    "flavours": ["Orange","Caramel"],
                },
            },
            "beerBadFlavour": {
                "summary": "Good flavour addition",
                "description": "This is a beer with an allowable list of flavours",
                "value": {
                    "name": "Hobgoblin",
                    "brewer": "Wychwood",
                    "strength": 4.3,
                    "flavours": ["Orange","Toothpaste"],
                },
            }
        },
    )):
    """Creates a new beer

    Args:
        beer (Beer): A beer object with the properties specified in the schemas.

    Returns:
        string: Description of whether beer is added.
    """
    if beer not in beer_list:
        beer_list.append(beer) 
        content = f'Beer "{beer.name}" Added.'
        response.status_code=status.HTTP_201_CREATED
        return content