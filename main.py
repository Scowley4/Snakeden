import menu
from chutesandladders import sl

def main():
    arcade = menu.Menu()
    game_selection = arcade.start_screen()
    print(game_selection)
    if game_selection == 'mario':
        pass
    elif game_selection == 's&l':
        print("here")
        sl.start()
        print("here2")
        

if __name__ == '__main__':
    main()

