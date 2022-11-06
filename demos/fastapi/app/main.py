from beer import Beer, Flavour, BeerList
from fastapi import FastAPI, status, Response, Body


beer1 = Beer(name="Mike Rayer",brewer="Crafty Devil",strength=4.6
                           , flavours=[Flavour.CARAMEL])
beer_list = BeerList([beer1])

app = FastAPI()

@app.get("/")
async def welcome():
    """Welcomes you to the beer API

    Returns:
        string: Welcome message
    """
    return "Welcome to the beer API!"

@app.post("/beers/")
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
    """Creates a new beer

    Args:
        beer (Beer): A beer object with the properties specified in the schemas.

    Returns:
        string: Description of whether beer is added.
    """
    response.status_code=status.HTTP_204_NO_CONTENT
    if beer_list.append(beer) is True:
        content = f'Beer "{beer.name}" Added.'
        response.status_code=status.HTTP_201_CREATED
        return content

@app.get("/beers/")
async def get_beers(response: Response):
    """Returns all available beers

    Returns:
        list[Beer]: Returns a list of beer objects
    """
    response.status_code=status.HTTP_200_OK
    return beer_list

@app.get("/beers/{name}/")
async def get_beer(response: Response,name: str):
    """Returns beer specified in path parameter

    Returns:
        Beer: Returns the beer object requested
    """
    beer = beer_list.get_beer_by_name(name)
    response.status_code=status.HTTP_200_OK
    return beer

@app.delete("/beers/{name}/")
async def delete_beer(response: Response, name: str):
    """Deletes the beer specified in the path parameter

    Returns:
        string: Description of whether beer is removed.
    """
    response.status_code=status.HTTP_204_NO_CONTENT
    if beer_list.remove_beer_by_name(name) is True:
        response.status_code=status.HTTP_200_OK
        content = f'Beer "{name}" removed.'
        return content

@app.put("/beers/{name}/")
async def set_beer(response: Response, name: str, beer: Beer= Body(
        examples={
            "normal": {
                "summary": "A normal beer",
                "description": "A **normal** beer will update correctly.",
                "value": {
                    "name": "Mike Rayer",
                    "brewer": "Crafty Devil",
                    "strength": 5.0,
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
    """Updates based on name of beer provided or creates beer if does not exist

    Returns:
        string: Description of whether beer is updated or created.
    """
    try:
        if beer_list.set_beer_by_name(name, beer) is True:
            content = f'Beer "{name}" updated.'
            response.status_code=status.HTTP_200_OK
        else:
            response.status_code=status.HTTP_201_CREATED
            content = f'Beer "{name}" created.'
    except ValueError as error:
        response.status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        content = repr(error)

    return content
