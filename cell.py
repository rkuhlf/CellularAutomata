import pygame


class Cell:
    def __init__(self, screen, x, y, w, h):
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.screen = screen
        self.activated = False
        self.next_phase = False

    def within_bounds(self, pos):
        x = pos[0]
        y = pos[1]
        if x > self.x + self.width:
            return False
        if x < self.x:
            return False
        if y < self.y:
            return False
        if y > self.y + self.height:
            return False

        return True

    def render(self):
        color = pygame.Color(255, 255, 255)
        if (self.activated):
            color = pygame.Color(0, 0, 0)
        pygame.draw.rect(self.screen, color, (self.x, self.y, self.width, self.height))

    def handle_click(self, pos):
        if (self.within_bounds(pos)):
            self.activated = not self.activated

    def get_next_phase(self, rules, data):
        self.next_phase = False
        for rule in rules:
            temp = True
            for row_index in range(len(data)):
                for col_index in range(len(data[row_index])):
                    if rule[row_index][col_index] != 2 and data[row_index][col_index] != rule[row_index][col_index]:
                        temp = False
            if temp:
                self.next_phase = True

    def trigger_next_phase(self):
        self.activated = self.next_phase
