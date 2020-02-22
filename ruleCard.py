import pygame


class RuleCard:
    def __init__(self, screen, data, x=False, y=False):
        self.data = data
        self.screen = screen
        if not x:
            self.x = screen.get_width() / 2
        else:
            self.x = x
        if not y:
            self.y = screen.get_height() / 2
        else:
            self.y = y

        self.cell_size = 100

        print(self.y)

    def render(self):
        for row_index in range(len(self.data)):
            for col_index in range(len(self.data[row_index])):
                color = pygame.Color(255, 255, 255)
                if self.data[row_index][col_index] == 1:
                    color = pygame.Color(0, 0, 0)
                elif self.data[row_index][col_index] == 2:
                    color = pygame.Color(127, 127, 127)
                cell_size = self.cell_size
                x = (col_index - len(self.data[row_index]) / 2) * cell_size + self.x
                y = (row_index - len(self.data) / 2) * cell_size + self.y
                pygame.draw.rect(self.screen, color, (x, y, cell_size, cell_size))

    def get_click_index(self, pos):
        clickx, clicky = pos
        x = -1
        y = -1
        cell_size = self.cell_size
        for row_index in range(len(self.data)):
            for col_index in range(len(self.data[row_index])):
                minx = (row_index - len(self.data) / 2) * cell_size + self.x
                maxx = minx + cell_size
                miny = (col_index - len(self.data[row_index]) / 2) * cell_size + self.y
                maxy = miny + cell_size
                if maxx > clickx > minx:
                    x = row_index

                if maxy > clicky > miny:
                    y = col_index
        return x, y

    def handle_click(self, pos, edit_rules_function, click_type):
        # eventually have click type to determine what to set the cell to
        x, y = self.get_click_index(pos)
        print(x, y)
        if x != -1 and y != -1:
            edit_rules_function(x, y, click_type)
