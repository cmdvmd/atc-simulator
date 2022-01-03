import pygame
import assets
import random
import math
import main
import game


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

    def draw(self, surface, pos=(0, 0)):
        """
        Draw button on screen

        :param surface: Surface to draw graphic onto
        :param pos: Position of surface on the window (defaults to (0, 0) for the window itself)
        """

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_x -= pos[0]
        mouse_y -= pos[1]

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

    def collide_end(self, x, y):
        if self.width >= self.height and self.y <= y <= self.y + self.runway_width:
            if self.x <= x <= self.x + self.runway_width:
                return self, 0
            elif self.x + self.width - self.runway_width <= x <= self.x + self.width:
                return self, 180
            else:
                return None, -1
        elif self.height > self.width and self.x <= x <= self.x + self.runway_width:
            if self.y <= y <= self.y + self.runway_width:
                return self, 270
            elif self.y + self.height - self.runway_width <= y <= self.y + self.height:
                return self, 90
            else:
                return None, -1
        else:
            return None, -1

    def draw(self, surface):
        """
        Draw runway on screen

        :param surface: Surface to draw graphic onto
        """

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


class Airplane:
    def __init__(self, image):
        self.image = image
        self.angle = 0
        self.x = 0
        self.y = 0
        self.normal_size = 50
        self.grounded_size = 30
        self.path = []
        self.last_movement = main.get_time()
        self.color = []
        self.grounded = False
        self.clicked = False
        self.runway = None
        self.runway_angle = -1
        self.gate_number = None
        self.gate_y = None
        self.gate_angle = None
        self.at_gate = None
        self.gate = False
        self.parked = False
        self.ready = True
        self.added_balance = False
        self.movement_interval = None
        self.gate_time = None
        self.runway_size = None
        self.runway_revenue = None
        self.gate_revenue = None
        self.penalty = None

        self.size_based_stats()

        for _ in range(3):
            self.color.append(random.randint(0, 175))

    def size_based_stats(self):
        if self.image == assets.LARGE_PLANE:
            self.movement_interval = random.randint(25, 75)
            self.gate_time = random.randint(15000, 20000)
            self.runway_size = assets.LARGE_PLANE_RUNWAY
            self.runway_revenue = 50000
        elif self.image == assets.MEDIUM_PLANE:
            self.movement_interval = random.randint(100, 150)
            self.gate_time = random.randint(10000, 15000)
            self.runway_size = assets.MEDIUM_PLANE_RUNWAY
            self.runway_revenue = 25000
        else:
            self.movement_interval = random.randint(175, 225)
            self.gate_time = random.randint(5000, 10000)
            self.runway_size = assets.SMALL_PLANE_RUNWAY
            self.runway_revenue = 10000
        self.gate_revenue = self.runway_revenue * 2
        self.penalty = self.gate_revenue * 2

    def position_on_runway(self):
        """
        Position airplane in the middle of the runway
        """

        size = (self.grounded_size if self.grounded else self.normal_size) / 2
        if self.runway_angle == 0 or self.runway_angle == 180:
            self.y = self.runway.y + (self.runway.runway_width / 2) - size
        elif self.runway_angle == 90 or self.runway_angle == 270:
            self.x = self.runway.x + (self.runway.runway_width / 2) - size

    def draw(self, surface):
        """
        Draw airplane on screen

        :param surface: Surface to draw graphic onto
        """

        time = main.get_time()
        thickness = 1 if self.grounded else 2

        if not main.data[assets.GAME_OVER]:
            if self.path or (self.runway is None and not self.parked):
                if len(self.path) >= 2:
                    pygame.draw.lines(surface, self.color, False, self.path, thickness)

                if not (
                        -self.normal_size <= self.x <= surface.get_width() and -self.normal_size <= self.y <= surface.get_height()):
                    main.data[assets.AIRPLANES].remove(self)
                    if self.at_gate is None:
                        main.data[assets.BALANCE] -= self.penalty
                    else:
                        main.data[assets.SCORE] += 1

                if time - self.last_movement >= self.movement_interval and not self.clicked:
                    self.last_movement = time
                    if self.path:
                        del self.path[0]
                        if self.path:
                            offset = (self.grounded_size if self.grounded else self.normal_size) / 2
                            self.angle = math.atan2(self.y + offset - self.path[0][1], self.path[0][0] - self.x - offset)
                            self.x = self.path[0][0] - offset
                            self.y = self.path[0][1] - offset
                    elif not self.grounded:
                        self.x += math.cos(self.angle) * 3
                        self.y -= math.sin(self.angle) * 3
            else:
                self.grounded = True
                self.movement_interval = 400
                main.data[assets.AIRPLANES].insert(0,
                                                   main.data[assets.AIRPLANES].pop(main.data[assets.AIRPLANES].index(self)))

                self.position_on_runway()

                try:
                    if time - self.last_movement >= self.movement_interval:
                        if self.runway_angle == 0:
                            assert self.x <= self.runway.x + self.runway.width - self.grounded_size
                            self.x += 2
                        elif self.runway_angle == 180:
                            assert self.x >= self.runway.x
                            self.x -= 2
                        if self.runway_angle == 90:
                            assert self.y >= self.runway.y
                            self.y -= 2
                        elif self.runway_angle == 270:
                            assert self.y <= self.runway.y + self.runway.height - self.grounded_size
                            self.y += 2
                except AssertionError:
                    if self.at_gate is not None:
                        self.grounded = False
                        self.ready = False
                        self.size_based_stats()
                        self.position_on_runway()
                        main.data[assets.AIRPLANES].remove(self)
                        main.data[assets.AIRPLANES].append(self)
                    self.runway = None
                    main.data[assets.BALANCE] += self.runway_revenue

                if self.gate_number is not None:
                    if self.at_gate is None:
                        self.at_gate = time
                    self.ready = time - self.at_gate >= self.gate_time
                    if self.ready:
                        self.parked = False
                        if not self.added_balance:
                            main.data[assets.BALANCE] += self.gate_revenue
                            self.added_balance = True

                if self.runway is not None:
                    self.angle = math.radians(self.runway_angle)

            if not self.path and self.gate and self.gate_number is not None:
                self.x = game.gates[self.gate_number]
                self.y = self.gate_y
                self.angle = math.radians(self.gate_angle)

        image = pygame.transform.rotate(
            pygame.transform.scale(pygame.image.fromstring(self.image, assets.PLANE_SIZE, 'RGBA'),
                                   (self.grounded_size, self.grounded_size) if self.grounded else (
                                   self.normal_size, self.normal_size)), math.degrees(self.angle) - 90)
        mask = pygame.Surface(image.get_size()).convert_alpha()
        mask.fill(self.color)

        if game.hitboxes:
            pygame.draw.rect(surface, assets.INFO_ERROR_COLOR, self.get_rect(), thickness)
        if self.ready or self.color == assets.AIRPLANE_COLLISION_COLOR:
            image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        surface.blit(image, (self.x, self.y))

    def get_rect(self):
        """
        Get pygame hit box of airplane
        """

        return pygame.Rect((self.x, self.y), (self.grounded_size, self.grounded_size) if self.grounded else (
            self.normal_size, self.normal_size))

    @staticmethod
    def generate_airplane():
        """
        Generate an airplane at a random position on the perimeter of the screen
        """

        airplane = Airplane(random.choice([assets.SMALL_PLANE, assets.MEDIUM_PLANE, assets.LARGE_PLANE]))

        top = bool(random.getrandbits(1))
        if top:
            airplane.y = random.choice([0, main.SCREEN_HEIGHT])
            airplane.x = random.randint(0, main.SCREEN_WIDTH - airplane.normal_size)
        else:
            airplane.x = random.choice([0, main.SCREEN_WIDTH])
            airplane.y = random.randint(0, main.SCREEN_HEIGHT - airplane.normal_size)

        airplane.angle = math.atan2(airplane.y - main.SCREEN_CENTER[1], main.SCREEN_CENTER[0] - airplane.x)

        main.data[assets.AIRPLANES].append(airplane)
