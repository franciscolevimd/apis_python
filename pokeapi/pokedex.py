import requests


URL = 'https://pokeapi.co/api/v2/pokemon'


def get_pokemons(limit=10, offset=0):
	parameters = {
					'limit':limit, 
					'offset':offset
				 }
	response = requests.get(URL, params=parameters)
	if response.status_code == 200:
		return [pokemon.get('name') for pokemon in response.json().get('results', [])]
	else:
		print(f'Status code: {response.status_code}')


def list_pokemons():		
	get_pokemons()
	limit = 10
	offset = 0
	page = 1
	pokemons = get_pokemons()
	while True:
		for pokemon in pokemons:
			print(f'\t{pokemon}')
		print(f'\n[P]revious | p[A]ge {page} | [S]how {limit} pokemons | [N]ext | [B]ack to menu')
		option = input('# Select an option: ').upper()
		if option == 'P':
			print('Previous')
		elif option == 'A':
			print('Page')
		elif option == 'S':
			print('Limit')
		elif option == 'N':
			print('Next')		
		elif option == 'B':
			break
		else:
			print('Invalid option!')


def display_menu():
	print('''
	//////////////// POKEDEX //////////////// 
	-----------------------------------------
	[L]ist pokemons
	[F]ind pokemon
	[E]xit
	''')


def main():
	while True:
		display_menu()
		option = input('# Select an option: ').upper()
		if option == 'L':
			print('')
			list_pokemons()
		elif option == 'F':
			print('Find pokemons')
		elif option == 'E':
			break
		else:
			print('Invalid option!')


if __name__ == '__main__':
	main()