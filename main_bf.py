from configs import *


class App_BF:
    def __init__(self):
        self.cols, self.rows = 30, 20
        self.TITLE = 30
        pg.init()
        self.sc = pg.display.set_mode([self.cols * self.TITLE, self.rows * self.TITLE])
        self.clock = pg.time.Clock()
        self.option = 1
        self.grid = []

    def back_button(self, x, y):
        IMAGE = pg.image.load('img/back_button.png').convert()  # or .convert_alpha()
        rect = IMAGE.get_rect()
        rect.topleft = (x * self.TITLE, y * self.TITLE)
        self.sc.blit(IMAGE, rect)

    def undo_button(self, x, y):
        IMAGE = pg.image.load('img/clear_button.png').convert()  # or .convert_alpha()
        rect = IMAGE.get_rect()
        rect.topleft = (x * self.TITLE, y * self.TITLE)
        self.sc.blit(IMAGE, rect)

    def done_button(self, x, y):
        IMAGE = pg.image.load('img/done_button.png').convert()  # or .convert_alpha()
        rect = IMAGE.get_rect()
        rect.topleft = (x * self.TITLE, y * self.TITLE)
        self.sc.blit(IMAGE, rect)

    def ranzomize(self):
        self.grid = [[1 if random() < 0.25 else 0 for col in range(self.cols)] for row in range(self.rows)]
        self.grid[0][0] = 0

    def get_rect(self, x, y):
        return x * self.TITLE + 1, y * self.TITLE + 1, self.TITLE - 2, self.TITLE - 2

    def get_next_nodes(self, x, y):
        check_next_node = lambda x, y: True if 0 <= x < self.cols and 0 <= y < self.rows and not self.grid[y][
            x] else False
        ways = [-1, 0], [0, -1], [1, 0], [0, 1]
        ways_diago = [-1, 0], [0, -1], [1, 0], [0, 1], [-1, -1], [1, -1], [1, 1], [-1, 1]
        return [(x + dx, y + dy) for dx, dy in ways if check_next_node(x + dx, y + dy)]

    def get_click_mouse_pos(self):
        x, y = pg.mouse.get_pos()
        grid_x, grid_y = x // self.TITLE, y // self.TITLE
        pg.draw.rect(self.sc, pg.Color('darkorange'), self.get_rect(grid_x, grid_y))
        click = pg.mouse.get_pressed()
        return (grid_x, grid_y) if click[0] else False

    def get_click_mouse_pos_right(self):
        x, y = pg.mouse.get_pos()
        grid_x, grid_y = x // self.TITLE, y // self.TITLE
        # pg.draw.rect(sc, pg.Color('red'), get_rect(grid_x, grid_y))
        click = pg.mouse.get_pressed()
        return (grid_x, grid_y) if click[2] else False

    def bfs(self, start, goal, graph):
        queue = deque([start])
        visited = {start: None}
        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break
            next_nodes = graph[cur_node]
            for next_node in next_nodes:
                if next_node not in visited:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        return visited

    def Draw(self):
        self.grid = [[0 for col in range(self.cols)] for row in range(self.rows)]
        while True:
            self.sc.fill((35, 46, 30))
            # pg.draw.rect(self.sc, (43, 44, 48),(0,0, self.TITLE * self.cols,self.TITLE))
            [[pg.draw.rect(self.sc, pg.Color('green'), self.get_rect(x, y), border_radius=self.TITLE // 8)
              for x, col in enumerate(row) if col] for y, row in enumerate(self.grid)]

            # click stang i click drept
            mouse_pos_l = self.get_click_mouse_pos()
            mouse_pos_r = self.get_click_mouse_pos_right()
            if mouse_pos_l == (29, 0):
                break

            if mouse_pos_l == (28, 0):
                self.grid = [[0 for col in range(self.cols)] for row in range(self.rows)]

            if mouse_pos_l == (27, 0):
                self.menu()

            if mouse_pos_l:
                self.grid[mouse_pos_l[1]][mouse_pos_l[0]] = 1
                pg.draw.rect(self.sc, pg.Color('forestgreen'), self.get_rect(*mouse_pos_l),
                             border_radius=self.TITLE // 8)

            if mouse_pos_r:
                self.grid[mouse_pos_r[1]][mouse_pos_r[0]] = 0
                pg.draw.rect(self.sc, pg.Color('red'), self.get_rect(*mouse_pos_r), border_radius=self.TITLE // 8)

            pg.draw.rect(self.sc, pg.Color('blue'), self.get_rect(0, 0), border_radius=self.TITLE // 70)
            self.done_button(29, 0)
            self.undo_button(28, 0)
            self.back_button(27, 0)
            # pygame necesary lines
            [exit() for event in pg.event.get() if event.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick(100)

    def BFS(self):
        graph = {}
        for y, row in enumerate(self.grid):
            for x, col in enumerate(row):
                if not col:
                    graph[(x, y)] = graph.get((x, y), []) + self.get_next_nodes(x, y)

        # bfs settings
        start = (0, 0)
        goal = start
        queue = deque([start])
        visited = {start: None}
        vis = 0
        while True:
            # fill screen
            self.sc.fill((35, 46, 30))
            [[pg.draw.rect(self.sc, pg.Color('green'), self.get_rect(x, y), border_radius=self.TITLE // 8)
              for x, col in enumerate(row) if col] for y, row in enumerate(self.grid)]

            # bfs, get path to mouse click
            if vis < 10 and self.option == 2:
                mouse_pos = (0, 0)
                vis += 1
            else:
                mouse_pos = self.get_click_mouse_pos()

            if mouse_pos and not self.grid[mouse_pos[1]][mouse_pos[0]]:
                visited = self.bfs(start, mouse_pos, graph)
                goal = mouse_pos

            # draw path
            path_head, path_segment = goal, goal
            while path_segment and path_segment in visited:
                pg.draw.rect(self.sc, pg.Color('yellow'), self.get_rect(*path_segment), self.TITLE,
                             border_radius=self.TITLE // 20)
                path_segment = visited[path_segment]
            pg.draw.rect(self.sc, pg.Color('blue'), self.get_rect(*start), border_radius=self.TITLE // 3)
            pg.draw.rect(self.sc, pg.Color('red'), self.get_rect(*path_head), border_radius=self.TITLE // 3)

            # pygame necesary lines
            [exit() for event in pg.event.get() if event.type == pg.QUIT]
            pg.display.flip()
            self.clock.tick(30)

    def chose_option(self, value, difficulty):
        if difficulty == 1:
            self.option = 1
        else:
            self.option = 2

    def start_the_game(self):
        if self.option == 1:
            self.ranzomize()
        else:
            self.Draw()

        self.BFS()

    def menu(self):
        menu = pygame_menu.Menu(self.rows * self.TITLE, self.cols * self.TITLE, 'BFS'
                                , theme=pygame_menu.themes.THEME_DARK)
        menu.add_selector('Input Method:', [('Random', 1), ('Manual ', 2)], onchange=self.chose_option)
        menu.add_button('Start', self.start_the_game)
        menu.add_button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(self.sc)


if __name__ == '__main__':
    draw = App_BF()
    draw.menu()
