import requests
from service import get_data_paged, get_page, get_url


EXIT = 'E'
LIST = 'L'
LIMIT_DEFAULT = 10
PAGE_DEFAULT = 1


def list_pokemons():
	pokemons_by_page = LIMIT_DEFAULT
	page_number = PAGE_DEFAULT
	data_paged = get_data_paged(pokemons_by_page=LIMIT_DEFAULT)
	page = get_page(get_url(), data_paged, page_number)
	while True:		
		print(f'\tID\t| NAME\t\t| TYPES')
		print('*' * 100)
		for pokemon in page.get('content'):
			types_text = ', '.join(pokemon.get('types'))
			print(f'\t{pokemon.get("id")}\t| {pokemon.get("name")}\t| {types_text}')
		print('*' * 100)
		print(f'[P]revious | p[A]ge {page_number} | [S]how {pokemons_by_page} pokemons | [N]ext | [B]ack to menu | [E]xit')
		option = input('# Select an option: ').upper()
		if option == 'P':
			page = get_page(page.get('previous'), data_paged)
			page_number = page.get('number')
		elif option == 'A':
			page_number = int(input('# Page: '))
			page = get_page(get_url(), data_paged, page_number)
		elif option == 'S':
			print('Pokemons by page')
		elif option == 'N':
			page = get_page(page.get('next'), data_paged)
			page_number = page.get('number')
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