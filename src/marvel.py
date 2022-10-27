marvel_api_private_key = 'b05fd57951353f70975dfda609ca4b2366320cbb'
marvel_api_public_key = '5157291a0e2c905dab976d9d72e1aba9'
marvel_hash = '866cbc64c6d87d4162218a77b8fe3e5b'
timestamp = 1
# hash = timestamp + private key + public key
characters = f'https://gateway.marvel.com:443/v1/public/characters?ts={timestamp}&apikey={marvel_api_public_key}&hash={marvel_hash}'
