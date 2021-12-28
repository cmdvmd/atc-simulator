import pygame
import pickle
import sys
import assets
import menu


def get_ticks():
    return pygame.time.get_ticks() + data[assets.TICKS]


def save_game():
    """
    Save game data
    """

    data[assets.TICKS] = get_ticks()
    with open(assets.SAVE_FILE, 'wb') as file:
        pickle.dump(data, file)


def close():
    """
    Close pygame and the application
    """

    save_game()
    pygame.quit()
    sys.exit()


# Define window settings
FPS = 60
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

CLOCK = pygame.time.Clock()
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

data = {}

# Start game
if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    pygame.display.set_caption('ATC Simulator')
    pygame.display.set_icon(assets.ICON)

    pygame.mouse.set_cursor(*pygame.cursors.arrow)

    menu.menu()
