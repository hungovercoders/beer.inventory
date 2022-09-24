from flask import Flask, jsonify,request
import json
from flask_expects_json import expects_json
import sys

app = Flask(__name__)
 
schema = {
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
    return "Hello and welcome to to the beer API!"

@app.route('/beers/', methods=['GET','POST']) 
@expects_json(schema, ignore_for=['GET'])  
def beers():
    if request.method == 'GET':
        return jsonify(beer_list)

    if request.method == 'POST':
        new_beer = request.json
        if new_beer not in beer_list:
            beer_list.append(new_beer)
            content = 'Beer Added'
        else:
            content = 'Beer Already Exists'

        return content

@app.route('/beers/<name>', methods=['GET','PUT','DELETE']) 
@expects_json(schema, ignore_for=['GET'])  
def beer(name):
    try:
        beer = [beer for beer in beer_list if beer['name'].replace(' ','').lower() == name.lower()][0]
    except:
         return "Beer does not exist"
    if request.method == 'GET':
        return jsonify(beer)
    if request.method == 'PUT':
        for idx, item in enumerate(beer_list):
            if beer["name"] in item["name"]:
                updated_beer = request.json
                beer_list[idx] = updated_beer
        return "Beer updated"

    if request.method == 'DELETE':
        if beer in beer_list:
            beer_list.remove(beer)
            return "Beer removed"
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)

##http://127.0.0.1:5000/beers/