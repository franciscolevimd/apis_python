import requests
import re


URL = 'https://pokeapi.co/api/v2/pokemon'
CODE_200 = 200

POKEAPI_COUNT = 'count'
POKEAPI_NAME = 'name' 
POKEAPI_ID = 'id' 
POKEAPI_TYPE = 'type'
POKEAPI_TYPES = 'types'
POKEAPI_OFFSET = 'offset'
POKEAPI_LIMIT = 'limit'
POKEAPI_RESULTS = 'results'
POKEAPI_POKEMONS = 'pokemons'
POKEAPI_URL = 'url'
POKEAPI_HEIGHT = 'height'
POKEAPI_WEIGHT = 'weight'
POKEAPI_ABILITY = 'ability'
POKEAPI_ABILITIES = 'abilities'
POKEAPI_BASE_EXPERIENCE = 'base_experience'
POKEAPI_STATS = 'stats'
POKEAPI_STAT = 'stat'

POKEDEX_ID = 'id'
POKEDEX_NAME = 'name'
POKEDEX_TYPES = 'types'
POKEDEX_COUNT_PAGES = 'count_pages'
POKEDEX_COUNT_POKEMONS = 'count_pokemons'
POKEDEX_POKEMONS_BY_PAGE = 'pokemons_by_page'
POKEDEX_PREVIOUS = 'previous'
POKEDEX_NEXT = 'next'
POKEDEX_POKEMONS = 'pokemons'
POKEDEX_NUMBER = 'number'
POKEDEX_OFFSET = 'offset'
POKEDEX_CONTENT = 'content'
POKEDEX_HEIGHT = 'height'
POKEDEX_WEIGHT = 'weight'			
POKEDEX_ABILITIES = 'abilities'
POKEDEX_BASE_EXPERIENCE = 'base_experience'
POKEDEX_STATS = 'stats'


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
		pokemon = {POKEDEX_ID:pokemon_json.get(POKEAPI_ID), POKEDEX_NAME:pokemon_json.get(POKEAPI_NAME).capitalize()}
		pokemon[POKEDEX_TYPES] = [type_json.get(POKEAPI_TYPE).get(POKEAPI_NAME).capitalize() for type_json in pokemon_json.get(POKEAPI_TYPES, [])]
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
		count_pokemons = int(pokemons_json.get(POKEAPI_COUNT))
		count_pages = (count_pokemons // pokemons_by_page) + 1 if count_pokemons % pokemons_by_page > 0 else count_pokemons // pokemons_by_page
		return {POKEDEX_COUNT_POKEMONS:count_pokemons, POKEDEX_POKEMONS_BY_PAGE:pokemons_by_page, POKEDEX_COUNT_PAGES:count_pages}


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
	count_pages = data_paged.get(POKEDEX_COUNT_PAGES)		
	pokemons_by_page = data_paged.get(POKEDEX_POKEMONS_BY_PAGE)
	if page_number > count_pages:
		offset = (count_pages * pokemons_by_page) - pokemons_by_page
	elif 0 < page_number <= count_pages:		
		offset = pokemons_by_page * (page_number - 1)
	return {POKEAPI_LIMIT:pokemons_by_page, POKEAPI_OFFSET:offset}


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
		content_page.pop(POKEAPI_COUNT)
		pokemons = content_page.pop(POKEAPI_RESULTS)
		content_page[POKEAPI_POKEMONS] = [get_pokemon_header(pokemon.get(POKEAPI_URL)) for pokemon in pokemons]			
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
	pokemons_by_page = data_paged.get(POKEDEX_POKEMONS_BY_PAGE)
	last_page = data_paged.get(POKEDEX_COUNT_PAGES)
	offset = pokemons_by_page * (last_page - 1)
	if page_number == last_page:			
			content_page[POKEDEX_NEXT] = f'{URL}?offset=0&limit={pokemons_by_page}'
			content_page[POKEDEX_PREVIOUS] = f'{URL}?offset={offset - pokemons_by_page}&limit={pokemons_by_page}'
	elif page_number == 1:
			content_page[POKEDEX_PREVIOUS] = f'{URL}?offset={offset}&limit={data_paged.get(POKEDEX_COUNT_POKEMONS) - offset}'


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
		page_number = get_page_number(data_paged.get(POKEDEX_POKEMONS_BY_PAGE), url)

	if content_page and content_page.get(POKEDEX_POKEMONS):
		__format_content_page(content_page, data_paged, page_number)
		page = {
			POKEDEX_NUMBER:page_number, 
			POKEDEX_OFFSET:data_paged.get(POKEDEX_POKEMONS_BY_PAGE) * (page_number - 1),
			POKEDEX_NEXT:content_page.pop(POKEDEX_NEXT), 
			POKEDEX_PREVIOUS:content_page.pop(POKEDEX_PREVIOUS), 
			POKEDEX_CONTENT:content_page.pop(POKEDEX_POKEMONS)
		}
	return page


def get_pokemon_by(id=None, name=None):
	"""Retrieves the pokemon data by its id or name.

	Args:
		id (int) - Pokemon id.
		name (str) - Pokemon name.

	Returns:
		dict: Pokemon data: 
		{
			'id': 12, 
			'name': 'butterfree', 
			'height': 11, 
			'weight': 320, 
			'types': ['bug', 'flying'], 
			'abilities': ['compound-eyes', 'tinted-lens'], 
			'base_experience': 178, 
			'stats': [
				{
					'base_stat': 60, 
					'effort': 0, 
					'name': 'hp'
				}, 
				{
					'base_stat': 45, 
					'effort': 0, 
					'name': 'attack'
				}, 
				{
					'base_stat': 50, 
					'effort': 0, 
					'name': 'defense'
				}, 
				{
					'base_stat': 90, 
					'effort': 2, 
					'name': 'special-attack'
				}, 
				{
					'base_stat': 80, 
					'effort': 1, 
					'name': 'special-defense'
				}, 
				{
					'base_stat': 70, 
					'effort': 0, 
					'name': 'speed'
				}
			]
		}
	"""	
	if id:
		response = requests.get(f'{URL}/{id}')
	elif name:
		response = requests.get(f'{URL}/{name.lower()}')
	pokemon = {}
	if response.status_code == CODE_200:
		pokemon_json = response.json()
		pokemon[POKEDEX_ID] = pokemon_json.get(POKEAPI_ID)
		pokemon[POKEDEX_NAME] = pokemon_json.get(POKEAPI_NAME).capitalize()
		pokemon[POKEDEX_HEIGHT] = pokemon_json.get(POKEAPI_HEIGHT)
		pokemon[POKEDEX_WEIGHT] = pokemon_json.get(POKEAPI_WEIGHT)
		pokemon[POKEDEX_TYPES] = [type_json.get(POKEAPI_TYPE).get(POKEAPI_NAME).capitalize() for type_json in pokemon_json.get(POKEAPI_TYPES)]
		pokemon[POKEDEX_ABILITIES] = [ability_json.get(POKEAPI_ABILITY).get(POKEAPI_NAME).capitalize() for ability_json in pokemon_json.get(POKEAPI_ABILITIES)]
		pokemon[POKEDEX_BASE_EXPERIENCE] = pokemon_json.get(POKEAPI_BASE_EXPERIENCE)
		stats = []
		for stat_json in pokemon_json.get(POKEAPI_STATS):
			stat_json[POKEDEX_NAME] = stat_json.pop(POKEAPI_STAT).get(POKEAPI_NAME).capitalize()
			stats.append(stat_json) 
		pokemon[POKEAPI_STATS] = stats
	return pokemon


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


