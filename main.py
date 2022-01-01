import pygame
import time
import pickle
import sys
import assets
import menu


def get_time():
    """
    Get time (in milliseconds) elapsed since start of game
    """

    return (time.time_ns() / 1000000) - (game_start_time / 1000000) + data[assets.GAME_TIME]


def save_game():
    """
    Save game data
    """

    if data:
        data[assets.GAME_TIME] = get_time()
        data[assets.HIGH_SCORE] = max(data[assets.HIGH_SCORE], data[assets.SCORE])
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
SCREEN_CENTER = SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2

CLOCK = pygame.time.Clock()
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

data = {}

game_start_time = 0

# Start game
if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    pygame.display.set_caption('ATC Simulator')
    pygame.display.set_icon(assets.ICON)

    pygame.mouse.set_cursor(*pygame.cursors.arrow)

    menu.menu()
