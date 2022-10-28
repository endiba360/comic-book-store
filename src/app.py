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
        return jsonify({'message': 'Something went wrong...', 'code': response_json['code']})

@app.route('/searchComics/comic/<string:comic_name>', methods=['GET'])
def fetch_one_comic(comic_name):
    name = comic_name
    # In order to find comic name, check if name contains any white space and replace it
    if ' ' in name:
        name.replace(' ', '%20')
        
    query_one_by_name = f'https://gateway.marvel.com:443/v1/public/comics?ts={marvel_timestamp}&title={name}&apikey={marvel_api_public_key}&hash={marvel_hash}'
    response = requests.get(query_one_by_name)
    response_json = response.json()
    
    if response_json['code'] == 200:
        match_comic = response_json['data']['results']
        # Check if our array of matched comics is empty
        if not match_comic:
            return jsonify({'message': 'There are no matches, please try again'})
        # One match could have multiple results
        list_of_comics = []
        for comic in match_comic:
            processed_comic = {}
            processed_comic['id'] = comic['id']
            processed_comic['title'] = comic['title']
            processed_comic['image'] = comic['thumbnail']['path']
            processed_comic['onSaleDate'] = comic['dates'][0]['date']
            print(processed_comic)
            # Check each element to avoid duplicates
            if processed_comic not in list_of_comics:
                list_of_comics.append(processed_comic)
        
        return list_of_comics
    else:
        return jsonify({'message': 'Something went wrong...', 'code': response_json['code']})

@app.route('/searchComics/character/<string:character_name>', methods=['GET'])
def fetch_one_character(character_name):
    name = character_name
    # In order to find character, check if name contains any white space and replace it
    if ' ' in name:
        name.replace(' ', '%20')
        
    query_one_by_name = f'https://gateway.marvel.com:443/v1/public/characters?ts={marvel_timestamp}&name={name}&apikey={marvel_api_public_key}&hash={marvel_hash}'
    response = requests.get(query_one_by_name)
    response_json = response.json()
    
    if response_json['code'] == 200:
        match_character = response_json['data']['results']
        
        if not match_character:
            return jsonify({'message': 'There are no matches, please try again'})
        
        processed_character = {}
        # Check each key of matched character to assign only required information
        for key in match_character:
            processed_character['id'] = key['id']
            processed_character['name'] = key['name']
            processed_character['image'] = key['thumbnail']['path']
            processed_character['appearances'] = key['comics']['available']
        print(processed_character)
        
        return processed_character
    else:
        return jsonify({'message': 'Something went wrong...', 'code': response_json['code']})
    

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)
    