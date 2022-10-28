import requests
from flask import Flask, jsonify
from marvel import characters, marvel_hash, marvel_api_public_key, marvel_timestamp

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

@app.route('/searchComics/<int:comic_id>', methods=['GET'])
def fetch_one_comic(comic_name):
    pass

@app.route('/searchComics/<string:character_name>', methods=['GET'])
def fetch_one_character(character_name):
    name = character_name
    query_one_by_name = f'https://gateway.marvel.com:443/v1/public/characters?ts={marvel_timestamp}&name={name}&apikey={marvel_api_public_key}&hash={marvel_hash}'
    response = requests.get(query_one_by_name)
    response_json = response.json()
    
    if response_json['code'] == 200:
        match_character = response_json['data']['results']
        processed_character = {}
        
        for key in match_character:
            processed_character['id'] = key['id']
            processed_character['name'] = key['name']
            processed_character['image'] = key['thumbnail']['path']
            processed_character['appearances'] = key['comics']['available']
        print(processed_character)
        
        return processed_character
    else:
        print('Something went wrong...')
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)
    