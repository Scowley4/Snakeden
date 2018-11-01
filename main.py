import menu


def main():
    arcade = menu.Menu
    game_selection = arcade.start_screen()
    if game_selection == 'mario':
        pass


if __name__ == '__main':
    main()

