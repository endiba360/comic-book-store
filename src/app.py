from flask import Flask, jsonify
import requests
from users import users
from marvel import characters


app = Flask(__name__)

@app.route('/', methods=['GET'])
def ping():
    return jsonify({"response": "hello flask!"})

@app.route('/users', methods=['GET'])
def users_handler():
    return jsonify({"users": users})

@app.route('/searchComics', methods=['GET'])
def fetch_all_characters():
    response = requests.get(characters)
    response_json = response.json()
    
    if response_json['code'] == 200:
        all_characters = response_json['data']['results']
        processed_characters = {}
        for character in all_characters:
            processed_characters['id'] = character['id']
            processed_characters['name'] = character['name']
            processed_characters['image'] = character['thumbnail']['path']
            processed_characters['appearances'] = character['comics']['available']
            print(processed_characters)
        return response_json['data']['results']
    else:
        print('Something went wrong')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)
    