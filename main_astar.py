from configs import *

class App_AS:
    def __init__(self):
        self.cols, self.rows = 30, 20
        self.TITLE = 30
        pg.init()
        self.sc = pg.display.set_mode([self.cols * self.TITLE, self.rows * self.TITLE])
        self.pondere = 2
        self.option = 1

    def get_click_mouse_pos(self):
        x, y = pg.mouse.get_pos()
        grid_x, grid_y = x // self.TITLE, y // self.TITLE
        # pg.draw.rect(self.sc, pg.Color('darkorange'), self.get_rect(grid_x, grid_y))
        if self.pondere == 1:  # drumul
            self.draw_road(grid_x, grid_y)
        if self.pondere == 8:  # apa
            self.draw_water(grid_x, grid_y)
        if self.pondere == 9:  # piatra
            self.draw_rock(grid_x, grid_y)
        if self.pondere == 3:  # iarba
            self.draw_grass(grid_x, grid_y)
        click = pg.mouse.get_pressed()
        return (grid_x, grid_y) if click[0] else False

    def get_click_mouse_pos_right(self):
        x, y = pg.mouse.get_pos()
        grid_x, grid_y = x // self.TITLE, y // self.TITLE
        # pg.draw.rect(sc, pg.Color('red'), get_rect(grid_x, grid_y))
        click = pg.mouse.get_pressed()
        return (grid_x, grid_y) if click[2] else False

    def draw_done_button(self,x,y):
        IMAGE = pg.image.load('img/done_button.png').convert()  # or .convert_alpha()
        rect = IMAGE.get_rect()
        rect.topleft = (x * self.TITLE, y * self.TITLE)
        self.sc.blit(IMAGE, rect)

    def back_button(self,x,y):
        IMAGE = pg.image.load('img/back_button.png').convert()  # or .convert_alpha()
        rect = IMAGE.get_rect()
        rect.topleft = (x * self.TITLE, y * self.TITLE)
        self.sc.blit(IMAGE, rect)

    def undo_button(self,x,y):
        IMAGE = pg.image.load('img/clear_button.png').convert()  # or .convert_alpha()
        rect = IMAGE.get_rect()
        rect.topleft = (x * self.TITLE, y * self.TITLE)
        self.sc.blit(IMAGE, rect)

    def get_circle(self, x, y):
        return (x * self.TITLE + self.TITLE // 2, y * self.TITLE + self.TITLE // 2), self.TITLE // 4

    def get_rect(self, x, y):
        return x * self.TITLE + 1, y * self.TITLE + 1, self.TITLE - 2, self.TITLE - 2

    def draw_rock(self, x, y):
        IMAGE = pg.image.load('img/rock.png').convert()  # or .convert_alpha()
        rect = IMAGE.get_rect()
        rect.topleft = (x * self.TITLE, y * self.TITLE)
        self.sc.blit(IMAGE, rect)
        # pg.draw.rect(self.sc, (145, 124, 111), self.get_rect(x, y), border_radius=self.TITLE // 8)

    def draw_water(self, x, y):
        IMAGE = pg.image.load('img/water.png').convert()  # or .convert_alpha()
        rect = IMAGE.get_rect()
        rect.topleft = (x * self.TITLE, y * self.TITLE)
        self.sc.blit(IMAGE, rect)
        # pg.draw.rect(self.sc, (18, 173, 130), self.get_rect(x, y), border_radius=self.TITLE // 8)

    def heuristic(self,a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def draw_road(self, x, y):
        IMAGE = pg.image.load('img/road.png').convert()  # or .convert_alpha()
        rect = IMAGE.get_rect()
        rect.topleft = (x * self.TITLE, y * self.TITLE)
        self.sc.blit(IMAGE, rect)

    def draw_grass(self, x, y):
        IMAGE = pg.image.load('img/grass.png').convert()  # or .convert_alpha()
        rect = IMAGE.get_rect()
        rect.topleft = (x * self.TITLE, y * self.TITLE)
        self.sc.blit(IMAGE, rect)

    def draw_word(self, x, y):
        IMAGE = pg.image.load('img/alege2.png').convert()  # or .convert_alpha()
        rect = IMAGE.get_rect()
        rect.topleft = (x * self.TITLE, y * self.TITLE)
        self.sc.blit(IMAGE, rect)

    def get_next_nodes(self, x, y):
        check_next_node = lambda x, y: True if 0 <= x < self.cols and 0 <= y < self.rows else False
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        return [(self.grid[y + dy][x + dx], (x + dx, y + dy)) for dx, dy in ways if check_next_node(x + dx, y + dy)]

    def Draw_Map(self):
        pg.init()
        clock = pg.time.Clock()
        while True:
            # fill screen
            self.sc.fill((143, 173, 18))
            # click stang i click drept
            mouse_pos_l = self.get_click_mouse_pos()
            mouse_pos_r = self.get_click_mouse_pos_right()
            if mouse_pos_l == (29, 0):
                self.Draw_Path()
            if mouse_pos_l == (28, 0):
                # self.undo_button(28,0)
                # self.menu()
                grid = dijkstra_conf.grid2
                self.grid = [[int(char) for char in string] for string in grid]
            if mouse_pos_l == (27, 0):
                self.menu()
            if mouse_pos_l == (16, 0):
                self.pondere = 9
            if mouse_pos_l == (15, 0):
                self.pondere = 8
            if mouse_pos_l == (14, 0):
                self.pondere = 3
            if mouse_pos_l == (13, 0):
                self.pondere = 1

            if mouse_pos_l:
                self.grid[mouse_pos_l[1]][mouse_pos_l[0]] = self.pondere
                pg.draw.rect(self.sc, pg.Color('forestgreen'), self.get_rect(*mouse_pos_l),
                             border_radius=self.TITLE // 8)

            if mouse_pos_r:
                self.grid[mouse_pos_r[1]][mouse_pos_r[0]] = 2
                pg.draw.rect(self.sc, pg.Color('red'), self.get_rect(*mouse_pos_r), border_radius=self.TITLE // 8)

            for y, row in enumerate(self.grid):
                for x, col in enumerate(row):
                    if col == 1:  # drumul
                        self.draw_road(x, y)
                    if col == 8:  # apa
                        self.draw_water(x, y)
                    if col == 9:  # piatra
                        self.draw_rock(x, y)
                    if col == 3:  # iarba
                        self.draw_grass(x, y)

            self.draw_done_button(29,0)
            self.undo_button(28, 0)
            self.back_button(27, 0)

            self.draw_word(12, 0)
            self.draw_road(13, 0)
            self.draw_grass(14, 0)
            self.draw_water(15,0)
            self.draw_rock(16,0)
            # pygame necessary lines
            [exit() for event in pg.event.get() if event.type == pg.QUIT]
            pg.display.flip()
            clock.tick(30)

    def Draw_Path(self):
        clock = pg.time.Clock()
        for i in range(13,17):
            self.grid[0][i] = 2

        # dict of adjacency lists
        graph = {}
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                graph[(x, y)] = graph.get((x, y), []) + self.get_next_nodes(x, y)

        start = (0, 9)
        goal = (29, 9)
        queue = []
        heappush(queue, (0, start))
        cost_visited = {start: 0}
        visited = {start: None}

        while True:
            # fill screen
            self.sc.fill((143, 173, 18))
            # [pg.draw.rect(self.sc, pg.Color('forestgreen'), self.get_rect(x, y), 1) for x, y in visited] # arata drumul vizitat

            for y, row in enumerate(self.grid):
                for x, col in enumerate(row):
                    if col == 1:  # drumul
                        self.draw_road(x, y)
                    if col == 8:  # apa
                        self.draw_water(x, y)
                    if col == 9:  # piatra
                        self.draw_rock(x, y)
                    if col == 3:  # iarba
                        self.draw_grass(x, y)

            # A* logic
            if queue:
                cur_cost, cur_node = heappop(queue)
                if cur_node == goal:
                    queue = []
                    continue
                next_nodes = graph[cur_node]
                for next_node in next_nodes:
                    neigh_cost, neigh_node = next_node
                    new_cost = cost_visited[cur_node] + neigh_cost
                    if neigh_node not in cost_visited or new_cost < cost_visited[neigh_node]:
                        priority = new_cost + self.heuristic(neigh_node, goal)
                        heappush(queue, (priority, neigh_node))
                        cost_visited[neigh_node] = new_cost
                        visited[neigh_node] = cur_node

            # draw path
            path_head, path_segment = cur_node, cur_node
            while path_segment:
                pg.draw.circle(self.sc, pg.Color('yellow'), *self.get_circle(*path_segment))
                path_segment = visited[path_segment]
            pg.draw.circle(self.sc, pg.Color('blue'), *self.get_circle(*start))
            pg.draw.circle(self.sc, pg.Color('red'), *self.get_circle(*path_head))
            # pygame necessary lines
            [exit() for event in pg.event.get() if event.type == pg.QUIT]
            pg.display.flip()
            clock.tick(30)
    def chose_option(self, value, difficulty):
        if difficulty == 1:
            self.option = 1
        else:
            self.option = 2

    def start_the_game(self):
        if self.option == 1:
            grid = dijkstra_conf.grid
            self.grid = [[int(char) for char in string] for string in grid]
            self.Draw_Path()
        else:
            grid = dijkstra_conf.grid2
            self.grid = [[int(char) for char in string] for string in grid]
            self.Draw_Map()


    def menu(self):
        menu = pygame_menu.Menu(self.rows * self.TITLE, self.cols * self.TITLE,  'A*'
                                ,theme=pygame_menu.themes.THEME_DARK)
        menu.add_selector('Input Method:', [('Default', 1), ('Manual ', 2)], onchange=self.chose_option)
        menu.add_button('Start', self.start_the_game)
        menu.add_button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.sc)


if __name__ == '__main__':
    draw = App_AS()
    draw.menu()
