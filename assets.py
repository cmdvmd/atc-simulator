import pygame
import os

#
# Images
#

ICON = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'icon.png')), (32, 32))
MENU_IMAGE = pygame.image.load(os.path.join('assets', 'menu_image.png'))
SMALL_PLANE = pygame.image.load(os.path.join('assets', 'small_plane.png'))
MEDIUM_PLANE = pygame.image.load(os.path.join('assets', 'medium_plane.png'))
LARGE_PLANE = pygame.image.load(os.path.join('assets', 'large_plane.png'))

#
# Colors
#

MENU_COLOR = 70, 100, 150
MENU_TITLE_COLOR = 255, 255, 255
MENU_BUTTON_COLOR = 0, 55, 165
MENU_BUTTON_COLOR_OVER = 30, 90, 215
MENU_BUTTON_COLOR_DOWN = 95, 135, 220

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

BUTTON_FONT = pygame.font.SysFont('Arial', 20)
TITLE_FONT = pygame.font.SysFont('Arial Black', 50)
