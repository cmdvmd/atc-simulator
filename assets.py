import pygame
import os

#
# Images
#

ICON = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'icon.png')), (32, 32))
SMALL_PLANE = pygame.image.load(os.path.join('assets', 'small_plane.png'))
MEDIUM_PLANE = pygame.image.load(os.path.join('assets', 'medium_plane.png'))
LARGE_PLANE = pygame.image.load(os.path.join('assets', 'large_plane.png'))

#
# Colors
#

GRASS_COLOR = 0, 200, 0
ROAD_COLOR = 200, 195, 190
TERMINAL_COLOR = 100, 100, 100
GATE_COLOR = 255, 255, 255
BUTTON_COLOR = 100, 100, 100, 200
BUTTON_COLOR_OVER = 100, 100, 100, 150
BUTTON_COLOR_DOWN = 125, 125, 125, 150
BUTTON_TEXT_COLOR = 255, 255, 255

#
# Fonts
#

pygame.font.init()

ARIAL = pygame.font.SysFont('Arial', 20)
