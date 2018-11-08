import menu
#from chutesandladders import sl
from mario import game

def main():
    arcade = menu.Menu()
    game_selection = arcade.start_screen()
    print(game_selection)
    if game_selection == 'mario':
        game.start()
    elif game_selection == 's&l':
        print('start s&l')
        #sl.start()

if __name__ == '__main__':
    main()

