import pygame
import assets
import main
import graphics


def draw_title(title):
    """
    Render title at top of screem

    :param title: Title to be rendered on the screen
    """

    title = assets.TITLE_FONT.render(title, True, assets.MENU_TITLE_COLOR)
    main.WINDOW.blit(title, ((main.SCREEN_WIDTH / 2) - (title.get_width() / 2), 10))


def draw_text(text, starting_y):
    """

    :param text: Text to draw on screen
    :param starting_y: Y value to start text at
    """

    for index, line in enumerate(text.split('\n')):
        rendered = assets.INFO_FONT.render(line, True, assets.INFO_TEXT_COLOR)
        main.WINDOW.blit(rendered, (0, (index * rendered.get_height()) + starting_y))


def draw_runways():
    """
    Draw runways instructions
    """

    draw_title('Drawing Runways')
    draw_text('''
    Runways are not created at the start of the game, but airplanes need runways to take off and land. To draw
    a runway, click the draw runway button.
    
    
    Left click at the starting point of the runway and drag until the desired length. The runway will
    automatically detect orientation (horizontal/vertical). When drawing a runway, the price and maximum
    airplane size that can use it are displayed on top. Right click an existing runway to delete it and
    earn a full refund
    
    
    The reward for an airplane successfully taking off or landing is added to the balance when the airplane
    reaches the end of the runway. At this point, the plane will stop and await further guidance
    ''', 140)

    main.WINDOW.blit(assets.DRAW_RUNWAY_BUTTON, (850, 160))
    main.WINDOW.blit(assets.DRAWING_RUNWAY, (800, 260))
    main.WINDOW.blit(assets.AIRPLANE_RUNWAY, (800, 380))


def draw_airplanes():
    """
    Draw airplanes instructions
    """

    draw_title('Airplanes')
    draw_text('''
    There are 3 different sizes of airplanes, each requiring different runway sizes, travelling at different
    speeds, and needing different cool down times
    
    
    Left click on an airplane to draw a path for it to follow. Keep in mind, different sizes of airplanes
    will follow this path at different speeds. Right click while drawing a path to erase it
    
    
    An airplane must first be guided to land at a runway, then guided to a gate where it will stop for some
    time, depending on its size, before needing to be guided to a runway to take off.
    
    
    Airplanes can only collide if they are at the same altitude (airborne or grounded). If one plane is airborne
    and another is grounded, the airborne plane will fly above the grounded one. Grounded airplanes are drawn
    smaller than airborne ones to be distinguished from one another
    ''', 100)

    main.WINDOW.blit(
        pygame.transform.scale(pygame.image.fromstring(assets.SMALL_PLANE, assets.PLANE_SIZE, 'RGBA'), (50, 50)),
        (775, 115))
    main.WINDOW.blit(
        pygame.transform.scale(pygame.image.fromstring(assets.MEDIUM_PLANE, assets.PLANE_SIZE, 'RGBA'), (50, 50)),
        (850, 115))
    main.WINDOW.blit(
        pygame.transform.scale(pygame.image.fromstring(assets.LARGE_PLANE, assets.PLANE_SIZE, 'RGBA'), (50, 50)),
        (925, 115))

    main.WINDOW.blit(assets.AIRPLANE_PATH, (800, 210))
    main.WINDOW.blit(assets.AIRPLANE_GATE, (850, 300))
    main.WINDOW.blit(assets.AIRPLANE_ALTITUDES, (850, 400))


def draw_intro():
    """
    Draw intro instructions
    """

    draw_title('Intro')
    draw_text('''
    The goal of this game is to guide airplanes to land, park, and take off safely
    
    At the beginning of a new game, players have 30 seconds to prepare. During this
    time (and throughout the rest of the game), players can:
    
    1. Draw runways for planes to take off and land on
    2. Expand the terminal to create more gates 
    
    An airplane will spawn at a random position at the edge of the screen. At first,
    airplanes will spawn slowly, but the time between spawns decreases as time goes on
    
    Pressing the [Esc] key will return to the menu. If the game is exited, progress is
    saved and can be loaded at the next session. The game ends when two or more airplanes collide. 
    ''', 125)

    main.WINDOW.blit(assets.MENU_IMAGE, (625, 75))


def draw_buttons():
    """
    Draw buttons on screen
    """

    global screen
    global pressed

    # Draw exit button graphics
    exit_button.draw(main.WINDOW)
    main.WINDOW.blit(back_arrow, (exit_button.x + (exit_button.width / 2) - (back_arrow.get_width() / 2),
                                  exit_button.y + (exit_button.height / 2) - (back_arrow.get_height() / 2)))

    if screen != 0:
        # Draw back button graphics
        back_button.draw(main.WINDOW)
        main.WINDOW.blit(back_arrow, (back_button.x + (back_button.width / 2) - (back_arrow.get_width() / 2),
                                      back_button.y + (back_button.height / 2) - (back_arrow.get_height() / 2)))

        if back_button.clicked and not pressed:
            screen -= 1
            pressed = True
            back_button.clicked = False

    if screen != len(screens) - 1:
        # Draw next button graphics
        next_button.draw(main.WINDOW)
        main.WINDOW.blit(next_arrow, (next_button.x + (next_button.width / 2) - (next_arrow.get_width() / 2),
                                      next_button.y + (next_button.height / 2) - (next_arrow.get_height() / 2)))

        if next_button.clicked and not pressed:
            screen += 1
            pressed = True
            next_button.clicked = False


def instructions():
    """
    Show all rules
    """

    global screen
    global pressed

    screen = 0

    while not exit_button.clicked:
        main.CLOCK.tick(main.FPS)

        # Draw graphics on screen
        main.WINDOW.fill(assets.MENU_COLOR)
        screens[screen]()
        draw_buttons()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_button.clicked = True
                main.close()
            elif event.type == pygame.MOUSEBUTTONUP:
                pressed = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit_button.clicked = True
                elif event.key == pygame.K_RIGHT and screen != len(screens) - 1:
                    screen += 1
                elif event.key == pygame.K_LEFT and screen != 0:
                    screen -= 1

        pygame.display.flip()

    exit_button.clicked = False


# Define variables for screen navigation
screens = [draw_intro, draw_airplanes, draw_runways]
screen = 0
pressed = False

# Define buttons
button_size = 50
button_y = main.SCREEN_HEIGHT - button_size - 10
button_curve = 10

exit_button = graphics.Button(
    10,
    20,
    button_size,
    button_size,
    assets.TRANSPARENT_BUTTON_COLOR,
    assets.TRANSPARENT_BUTTON_COLOR_OVER,
    assets.TRANSPARENT_BUTTON_COLOR_DOWN,
    button_curve
)

back_button = graphics.Button(
    10,
    button_y,
    button_size,
    button_size,
    assets.TRANSPARENT_BUTTON_COLOR,
    assets.TRANSPARENT_BUTTON_COLOR_OVER,
    assets.TRANSPARENT_BUTTON_COLOR_DOWN,
    button_curve
)

next_button = graphics.Button(
    main.SCREEN_WIDTH - button_size - 10,
    button_y,
    button_size,
    button_size,
    assets.TRANSPARENT_BUTTON_COLOR,
    assets.TRANSPARENT_BUTTON_COLOR_OVER,
    assets.TRANSPARENT_BUTTON_COLOR_DOWN,
    button_curve
)

next_arrow = pygame.transform.scale(assets.NEXT_ARROW, (button_size / 2, button_size / 2))
back_arrow = pygame.transform.scale(assets.BACK_ARROW, (button_size / 2, button_size / 2))
