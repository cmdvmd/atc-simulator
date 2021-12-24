import pygame
import sys
import assets
import menu


def close():
    """
    Close pygame and the application
    """

    pygame.quit()
    sys.exit()


# Define window settings
FPS = 60
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

CLOCK = pygame.time.Clock()
WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

data = {
    assets.BALANCE: 5000000,
    assets.TERMINAL_SIZE: 150,
    assets.RUNWAYS: []
}

# Start game
if __name__ == '__main__':
    pygame.init()
    pygame.font.init()

    pygame.display.set_caption('ATC Simulator')
    pygame.display.set_icon(assets.ICON)

    pygame.mouse.set_cursor(*pygame.cursors.arrow)

    menu.menu()
