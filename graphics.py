import pygame


class Button(pygame.Surface):
    def __init__(self, x, y, width, height, color, color_over, color_down, curve):
        super().__init__((width, height), pygame.SRCALPHA)

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.color_over = color_over
        self.color_down = color_down
        self.curve = curve
        self.clicked = False

    def draw(self, surface):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height:
            self.clicked = False
            for button in pygame.mouse.get_pressed():
                self.clicked = self.clicked or button
            color = self.color_down if self.clicked else self.color_over
        else:
            color = self.color

        self.fill(color)
        surface.blit(self, (self.x, self.y))
