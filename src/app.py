from flask import Flask, jsonify
from marvel import characters
import requests


app = Flask(__name__)

@app.route('/', methods=['GET'])
def ping():
    return jsonify({"response": "hello flask!"})

@app.route('/searchComics/', methods=['GET'])
def fetch_all_characters():
    response = requests.get(characters)
    response_json = response.json()
    
    if response_json['code'] == 200:
        all_characters = response_json['data']['results']
        # Iterate to get only desired data from each character
        list_of_characters = []
        for character in all_characters:
            processed_character = {}
            processed_character['id'] = character['id']
            processed_character['name'] = character['name']
            processed_character['image'] = character['thumbnail']['path']
            processed_character['appearances'] = character['comics']['available']
            print(processed_character)
            # Check each element to avoid duplicates
            if processed_character not in list_of_characters:
                list_of_characters.append(processed_character)
                
        return list_of_characters
    else:
        print('Something went wrong...')

@app.route('/searchComics/<string:comic_name>', methods=['GET'])
def fetch_one_comic(comic_name):
    pass

@app.route('/searchComics/<string:character_name>', methods=['GET'])
def fetch_one_character(character_name):
    pass

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)
    