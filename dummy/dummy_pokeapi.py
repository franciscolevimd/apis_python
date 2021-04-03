import requests
import json


URL = 'https://pokeapi.co/api/v2/'
ENDPOINT_POKEMON = 'pokemon'


def check_requests():
	url = 'https://pokeapi.co/api/v2/pokemon'
	r = requests.get(url)
	print(r.status_code)
	print(r.headers['content-type'])
	print(r.encoding)
	print(r.text)
	print('-------------------------------------------------------------')
	print(r.json())


def get_pokemon(id):
	parameters = {
					'id':1
				 }
	response = requests.get(f'{URL}{ENDPOINT_POKEMON}/{id}/')
	if response.status_code == 200:
		return response.json().get('name')


def get_pokemons(limit=10, offset=0):
	parameters = {
					'limit':limit, 
					'offset':offset
				 }
	response = requests.get(URL + ENDPOINT_POKEMON, params=parameters)
	if response.status_code == 200:
		return [pokemon.get('name') for pokemon in response.json().get('results', [])]


def main():
	# check_requests()	
	#print(get_pokemons(limit=4, offset=105))
	print(get_pokemon(105))


if __name__ == '__main__':
	main()