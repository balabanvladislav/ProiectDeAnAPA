from main_dijkstra import *
from main_astar import *
from main_bf import *

class App():
    def __init__(self):
        self.cols, self.rows = 30, 20
        self.TITLE = 30
        pg.init()
        self.sc = pg.display.set_mode([self.cols * self.TITLE, self.rows * self.TITLE])
        self.c = 1
    def chose_option(self, value, difficulty):
        if difficulty == 1:
            self.c = 1
        elif difficulty == 2:
            self.c = 2
        else:
            self.c = 3


    def start_the_game(self):
        if self.c == 1: # BFS
            draw = App_BF()
            draw.menu()
        elif self.c == 2:  # Djk
            draw = App_Djk()
            draw.menu()
        else:
            draw = App_AS()
            draw.menu()


    def menu(self):
        menu = pygame_menu.Menu(self.rows * self.TITLE, self.cols * self.TITLE,  'Menu'
                                ,theme=pygame_menu.themes.THEME_DARK)
        menu.add_selector('Select an algorithm:', [('     BF     ', 1), ('Dijkstra', 2), ('A*(star)',3)], onchange=self.chose_option)
        menu.add_button('Start', self.start_the_game)
        menu.add_button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.sc)


if __name__ == '__main__':
    draw = App()
    draw.menu()

