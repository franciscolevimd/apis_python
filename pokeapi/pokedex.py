def display_settings():
	pass


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
		option = input('Select an option: ').upper()
		if option == 'L':
			print('List pokemons')
		elif option == 'F':
			print('Find pokemons')
		elif option == 'E':
			break


if __name__ == '__main__':
	main()