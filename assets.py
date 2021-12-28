import pygame
import os

#
# Images
#

ICON = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'icon.png')), (32, 32))
MENU_IMAGE = pygame.image.load(os.path.join('assets', 'menu_image.png'))
SMALL_PLANE = pygame.image.tostring(pygame.image.load(os.path.join('assets', 'small_plane.png')), 'RGBA')
MEDIUM_PLANE = pygame.image.tostring(pygame.image.load(os.path.join('assets', 'medium_plane.png')), 'RGBA')
LARGE_PLANE = pygame.image.tostring(pygame.image.load(os.path.join('assets', 'large_plane.png')), 'RGBA')
PLANE_SIZE = 100, 100

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
INFO_TEXT_COLOR = 255, 255, 255
INFO_ERROR_COLOR = 255, 0, 0
RUNWAY_COLOR = 0, 0, 0
RUNWAY_MARKINGS_COLOR = 255, 255, 255

#
# Fonts
#

pygame.font.init()

INFO_FONT = pygame.font.SysFont('Arial', 20)
BUTTON_FONT = pygame.font.SysFont('Arial', 15)
TITLE_FONT = pygame.font.SysFont('Arial Black', 50)

#
# Prices
#

TERMINAL_PRICE = 100000
RUNWAY_PRICE = 100

#
# Runway lengths
#

SMALL_PLANE_RUNWAY = 10000
MEDIUM_PLANE_RUNWAY = 15000
LARGE_PLANE_RUNWAY = 23000

#
# Events
#

GENERATE_AIRPLANE = pygame.USEREVENT
SPEED_GENERATION = pygame.USEREVENT + 1

#
# Data keys
#

BALANCE = 'balance'
TERMINAL_SIZE = 'terminal size'
RUNWAYS = 'runways'
AIRPLANES = 'airplanes'
TIMEOUT = 'timeout'
TICKS = 'ticks'
SAVE_FILE = 'savefile'
