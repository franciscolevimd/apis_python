import requests
from service import get_pokemon_header, get_pokemons


EXIT = 'E'
LIST = 'L'


def list_pokemons():		
	get_pokemons()
	limit = 10
	offset = 0
	page = 1
	pokemons = get_pokemons()
	while True:
		print(f'\tID\t| NAME\t\t| TYPES')
		print('*' * 100)
		for pokemon in pokemons:
			types_text = ', '.join(pokemon.get("types"))
			print(f'\t{pokemon.get("id")}\t| {pokemon.get("name")}\t| {types_text}')
		print('*' * 100)
		print(f'[P]revious | p[A]ge {page} | [S]how {limit} pokemons | [N]ext | [B]ack to menu | [E]xit')
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
			return
		elif option == EXIT:
			return EXIT
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
		if option == LIST:
			print('')
			if list_pokemons() == EXIT:
				break
		elif option == 'F':
			print('Find pokemons')
		elif option == EXIT:
			break
		else:
			print('Invalid option!')


if __name__ == '__main__':
	main()