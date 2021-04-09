import requests


URL = 'https://pokeapi.co/api/v2/pokemon'
CODE_200 = 200


def get_pokemon_header(url):
	response = requests.get(url)
	if response.status_code == CODE_200:
		pokemon_json = response.json()
		pokemon = {'id':pokemon_json.get('id'), 'name':pokemon_json.get('name').capitalize()}
		pokemon['types'] = [type_json.get('type').get('name').capitalize() for type_json in pokemon_json.get('types', [])]
		return pokemon
	else:
		print(f'Status code: {response.status_code}')


def get_pokemons(limit=10, offset=0):
	parameters = {
		'limit':limit, 
		'offset':offset
	}
	response = requests.get(URL, params=parameters)
	if response.status_code == CODE_200:
		pokemon_json = response.json()
		return [get_pokemon_header(pokemon_data.get('url')) for pokemon_data in pokemon_json.get('results', [])]
	else:
		print(f'Status code: {response.status_code}')



	# Pokedex sencilla:
	# Paginar lista de pokemones: se podrá decidir la cantidad de pokemons que se desean mostrar en cada página tenieno un límiti mínimo de 5 pokemons por página y un máximo de 20.
	# Se deben mostrat las cantidades de páginas que de acuerdo la cantidad de pokemons por páginas elegida.
	# Las páginas irán numeradas a partri del número 1.	
	# Se podrá navegar hacía atrá y adelante de la página.
	# Se podrá posicionar en una página esecífica elegida por el usuario.
	# Como PLUS si la página actual es la primera, el navegador hacia atrás podrá posicionarse en la última página.
	# Como PLUS si la página actual es la última, el navegador hacia adelante podrá posicionarse en la primer página.
	# Los datos en la lista mostrarán el nombre del pokemon y sus tipos.
	# SOLO ESTO NO COMPLIQUES EL EJEMPLO
	# *** Tener en cuenta que count tiene el total de pokemons conocidos.
	# *** También types contiene la lista de tipos a las que pertenece el pokemon, muestra el nombre.