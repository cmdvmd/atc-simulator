import pygame
import assets


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


class Runway:
    runway_width = 50
    marking_width = 2
    marking_height = 20
    dash_width = 4
    dash_height = 10

    def __init__(self, starting_pos, ending_pos):
        self.starting_pos = starting_pos
        self.ending_pos = ending_pos
        self.width = abs(ending_pos[0] - starting_pos[0])
        self.height = abs(ending_pos[1] - starting_pos[1])
        self.rect = None
        self.x = None
        self.y = None
        self.area = None
        self.price = None

    def draw(self, surface):
        if self.width >= self.height:
            tl_corner = min(self.starting_pos[0], self.ending_pos[0]), self.starting_pos[1]
            runway = pygame.Surface((self.width, self.runway_width))
            runway.fill(assets.RUNWAY_COLOR)

            for y in range(0, self.runway_width, self.marking_width * 2):
                pygame.draw.rect(runway, assets.RUNWAY_MARKINGS_COLOR, (0, y, self.marking_height, self.marking_width))
                pygame.draw.rect(runway, assets.RUNWAY_MARKINGS_COLOR,
                                 (self.width - self.marking_height, y, self.marking_height, self.marking_width))
            for x in range(self.marking_height + self.dash_height, self.width - self.marking_height - self.dash_height,
                           self.dash_height * 2):
                pygame.draw.rect(runway, assets.RUNWAY_MARKINGS_COLOR, (
                    x, int((self.runway_width / 2) - (self.dash_height / 2)), self.dash_height, self.dash_width))
        else:
            tl_corner = self.starting_pos[0], min(self.starting_pos[1], self.ending_pos[1])
            runway = pygame.Surface((self.runway_width, self.height))
            runway.fill(assets.RUNWAY_COLOR)

            for x in range(0, self.runway_width, self.marking_width * 2):
                pygame.draw.rect(runway, assets.RUNWAY_MARKINGS_COLOR, (x, 0, self.marking_width, self.marking_height))
                pygame.draw.rect(runway, assets.RUNWAY_MARKINGS_COLOR,
                                 (x, self.height - self.marking_height, self.marking_width, self.marking_height))
            for y in range(self.marking_height + self.dash_height, self.height - self.marking_height - self.dash_height,
                           self.dash_height * 2):
                pygame.draw.rect(runway, assets.RUNWAY_MARKINGS_COLOR, (
                    int((self.runway_width / 2) - (self.marking_width / 2)), y, self.dash_width, self.dash_height))

        self.x, self.y = tl_corner
        surface.blit(runway, tl_corner)
        self.rect = runway.get_rect()
        self.area = self.rect.width * self.rect.height
        self.price = self.area * assets.RUNWAY_PRICE
