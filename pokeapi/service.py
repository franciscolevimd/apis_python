import requests
import re


URL = 'https://pokeapi.co/api/v2/pokemon'
CODE_200 = 200


def get_url():
	"""Retrieves the url of pokepai.

Returns:
		stirng - The url of pokeapi.	
	"""
	return URL


def get_pokemon_header(url):
	"""Retrieves the basic data of a pokemon: id, name and types.

	Args:
		url (str) - Request of data to the pokeapi.

	Returns:
		dict: Basic data of the pokemon: 
		{
			'id':13,
			'name':'Weedle',
			'types':['Bug', 'Poison']
		}
	"""
	response = requests.get(url)
	if response.status_code == CODE_200:
		pokemon_json = response.json()
		pokemon = {'id':pokemon_json.get('id'), 'name':pokemon_json.get('name').capitalize()}
		pokemon['types'] = [type_json.get('type').get('name').capitalize() for type_json in pokemon_json.get('types', [])]
		return pokemon


def get_data_paged(pokemons_by_page):
	"""Retrieves the information of paged.

	Args:
		pokemons_by_page (int) - Limit of pokemons by page.

	Returns:
		dict - Data of paged: 
		{
			'count_pokemons':1118,			
			'pokemons_by_page':10,
			'count_pages':112
		}
	"""
	response = requests.get(URL)
	if response.status_code == CODE_200:		
		pokemons_json = response.json()		
		count_pokemons = int(pokemons_json.get('count'))
		count_pages = (count_pokemons // pokemons_by_page) + 1 if count_pokemons % pokemons_by_page > 0 else count_pokemons // pokemons_by_page		
		return {'count_pokemons':count_pokemons, 'pokemons_by_page':pokemons_by_page, 'count_pages':count_pages}


def get_page_number(pokemons_by_page, url):
	"""Generates the page number from the URL.

	Args:
		pokemons_by_page (int)
		url (str) - Url to retrieves the pokemons page.

	Returns: 
		int - Page number.
	"""
	pattern = re.compile(r'^.+offset=(\d+)&limit=\d+$')
	response = re.match(pattern, url)
	if response:
		offset = int(response.group(1))
		return (offset // pokemons_by_page) + 1



def get_page_parameters(data_paged, page_number):
	"""Retrieves the parameters to get a page by URL.

	Args:
		data_paged (dict) - See get_data_paged().
		page_number (int)

	Returns:
		dict - Parameters to the url: 
		{
			'limit':20,
			'offset':150
		}
	"""
	offset = 0
	count_pages = data_paged.get('count_pages')		
	pokemons_by_page = data_paged.get('pokemons_by_page')
	if page_number > count_pages:
		offset = (count_pages * pokemons_by_page) - pokemons_by_page
	elif 0 < page_number <= count_pages:		
		offset = pokemons_by_page * (page_number - 1)
	return {'limit':pokemons_by_page, 'offset':offset}


def get_content_page(url, parameters=None):
	"""Retrieves the list of pokemons and the next and previous url page. 

	Args:
		url (str) - URL of the page. 
		parameters (dict, optional) - Contains the parameter to request the pokemon page. See requests.get() 

	Returns:
		dict - Content page: 
		{
			'next':'next":"https://pokeapi.co/api/v2/pokemon?offset=1115&limit=3',
			'previous':'https://pokeapi.co/api/v2/pokemon?offset=1105&limit=5'
			'pokemons':[
				{
					'id': 10213, 
					'name': 'Grimmsnarl-gmax', 
					'types': ['Dark', 'Fairy']
				}, 
				{
					'id': 10214, 
					'name': 'Alcremie-gmax', 
					'types': ['Fairy']
				}, 
				{
					'id': 10215, 
					'name': 'Copperajah-gmax', 
					'types': ['Steel']
				}, 
				{
					'id': 10216, 'name': 
					'Duraludon-gmax', 
					'types': ['Steel', 'Dragon']
				}, 
				{
					'id': 10217, 
					'name': 'Eternatus-eternamax', 
					'types': ['Poison', 'Dragon']
				}
			]
		}
	"""
	response = requests.get(url, parameters)
	if response.status_code == CODE_200:
		content_page = response.json()	
		content_page.pop('count')
		pokemons = content_page.pop('results')
		content_page['pokemons'] = [get_pokemon_header(pokemon.get('url')) for pokemon in pokemons]			
		return content_page


def __format_content_page(content_page, data_paged, page_number):
	"""Auxiliar function to format the contnte page.

		Args:
		content_page (dict) - See get_content_page().
		data_paged (dict) - Contains total of pages and the number of pokemons by page -count_pages, pokemons_by_page-.
							See get_data_paged().
		page_number (int)

		Returns:
			dict - Content page.
	"""
	pokemons_by_page = data_paged.get("pokemons_by_page")
	last_page = data_paged.get('count_pages')
	offset = pokemons_by_page * (last_page - 1)
	if page_number == last_page:			
			content_page['next'] = f'https://pokeapi.co/api/v2/pokemon?offset=0&limit={pokemons_by_page}'
			content_page['previous'] = f'https://pokeapi.co/api/v2/pokemon?offset={offset - pokemons_by_page}&limit={pokemons_by_page}'
	elif page_number == 1:
			content_page['previous'] = f'https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={data_paged.get("count_pokemons") - offset}'


def get_page(url, data_paged, page_number=None):
	"""Retrieves a page with its pokemons list. 

	Args:
		url (str) - URL of the page. 
		data_paged (dict) - Contains total of pages and the number of pokemons by page -count_pages, pokemons_by_page-.
							See get_data_paged().
		page_number (int, optional)

	Returns:
		dict - Page: 
		{
			'number': 20, 
			'offset': 95, 
			'next': 'https://pokeapi.co/api/v2/pokemon?offset=100&limit=5', 
			'previous': 'https://pokeapi.co/api/v2/pokemon?offset=90&limit=5', 
			'content': [
				{
					'id': 96, 
					'name': 'Drowzee', 
					'types': ['Psychic']
				}, 
				{
					'id': 97, 
					'name': 'Hypno', 
					'types': ['Psychic']
				}, 
				{
					'id': 98, 
					'name': 'Krabby', 
					'types': ['Water']
				}, 
				{
					'id': 99, 
					'name': 'Kingler', 
					'types': ['Water']
				}, 
				{
					'id': 100, 
					'name': 'Voltorb', 
					'types': ['Electric']
				}
			]
		}		
	"""
	page = None
	content_page = None
	if page_number:
		content_page = get_content_page (
				url, 
				get_page_parameters(data_paged, page_number)
			)
	else:		
		content_page = get_content_page(url)
		page_number = get_page_number(data_paged.get('pokemons_by_page'), url)

	if content_page and content_page.get('pokemons'):
		__format_content_page(content_page, data_paged, page_number)
		page = {
			'number':page_number, 
			'offset':data_paged.get('pokemons_by_page') * (page_number - 1),
			'next':content_page.pop('next'), 
			'previous':content_page.pop('previous'), 
			'content':content_page.pop('pokemons')
		}
	return page


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


