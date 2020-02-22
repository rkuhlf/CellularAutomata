import pygame


class Button:
    def __init__(self, screen, font, x=200, y=200, width=50, height=50, text="Button", on_click=lambda: None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.on_click = on_click
        self.screen = screen
        self.font = font
        self.color = pygame.Color(200, 200, 200)

    def render(self):
        pygame.draw.rect(self.screen, self.color,
                         (self.x - self.width / 2, self.y - self.height / 2, self.width, self.height))
        text = self.font.render(self.text, True, pygame.Color(0, 0, 0))
        textRect = text.get_rect()

        # set the center of the rectangular object.
        textRect.center = (self.x, self.y)

        self.screen.blit(text, textRect)

    def handle_click(self, pos):
        if (self.within_bounds(pos)):
            self.on_click()

    def within_bounds(self, pos):
        x = pos[0]
        y = pos[1]
        if x > self.x + self.width / 2:
            return False
        if x < self.x - self.width / 2:
            return False
        if y < self.y - self.height / 2:
            return False
        if y > self.y + self.height / 2:
            return False

        return True
