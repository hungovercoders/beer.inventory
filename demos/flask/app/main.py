from flask import Flask, jsonify,request
from flask_expects_json import expects_json

app = Flask(__name__)

beer_schema = {
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "brewer": { "type": "string" },
    "strength": { "type": "string" },
  },
  "required": ["name","brewer"]
}

beer_list = [
    {
            "name": "Mike",
            "brewer": "Crafty Devil",
            "strength": "4.2"
    }
]
 
@app.route('/hello/', methods=['GET'])  
def hello():
    return 'Hello and welcome to to the beer API!'

@app.route('/beers/', methods=['GET','POST']) 
@expects_json(beer_schema, ignore_for=['GET'])  
def beers():
    if request.method == 'GET':
        return jsonify(beer_list)

    if request.method == 'POST':
        new_beer = request.json
        beer_name = new_beer['name']
        if new_beer not in beer_list:
            beer_list.append(new_beer)
            content = f'Beer "{beer_name}" Added.'
        else:
            content = f'Beer "{beer_name}" Already Exists.'

    return content

@app.route('/beers/<name>', methods=['GET','PUT','DELETE']) 
@expects_json(beer_schema, ignore_for=['GET','DELETE'])  
def beer(name):
    try:
        beer = [beer for beer in beer_list if beer['name'].replace(' ','').lower() == name.lower()][0]
    except:
        return f'Beer "{name}" does not exist.'

    if request.method == 'GET':
        return jsonify(beer)

    if request.method in ('PUT','DELETE'):
        for idx, item in enumerate(beer_list):
            if beer["name"] in item["name"]:
                beer_index = idx

        if request.method == 'PUT':
            updated_beer = request.json
            beer_list[beer_index] = updated_beer
            return f'Beer "{name}" updated.'

        if request.method == 'DELETE':
            if beer in beer_list:
                del beer_list[beer_index]
                return f'Beer "{name}" removed.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)