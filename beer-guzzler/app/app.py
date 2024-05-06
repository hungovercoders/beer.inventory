from bs4 import BeautifulSoup

def get_beer_config():
    url = "test/pages/test01.html"
    beers_class = "beers"
    beer_class = "beer"
    beer_config = {
        "name":
        {
            "dom_object": "p",
            "dom_identifier": "id",
            "identifier_value": "name"
        },
          "brewer":
        {
            "dom_object": "p",
            "dom_identifier": "id",
            "identifier_value": "brewer"
        },
          "strength":
        {
            "dom_object": "p",
            "dom_identifier": "id",
            "identifier_value": "strength"
        }
    }

    return url, beers_class, beer_class, beer_config

def guzzle_beer(url:str,beers_class: str, beer_class: str, beer_config: dict):

    beer_list = []
    with open(url) as page:
        soup = BeautifulSoup(page,"html.parser")
        contents = soup.find("div", class_=beers_class)
        beers = contents.find_all("div", {"class": beer_class})
        for beer in beers:
            beer_dict = {}
            for key in beer_config:
                dom_object = beer_config[key]["dom_object"]
                dom_identifier = beer_config[key]["dom_identifier"]
                identifier_value = beer_config[key]["identifier_value"]
                value = beer.find(dom_object, {dom_identifier: f"{identifier_value}"}).get_text()
                beer_dict.update({key:value})
            beer_list.append(beer_dict)

    return beer_list

if __name__ == '__main__':

    url, beers_class, beer_class, beer_config = get_beer_config()

    beer_list = guzzle_beer(url
    , beers_class=beers_class
    , beer_class=beer_class
    , beer_config=beer_config)

    print(beer_list)
  


