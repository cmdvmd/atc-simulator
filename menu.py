import pygame
import assets
import main
import graphics


def menu():
    """
    Run main menu loop
    """

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(main.FPS)

        # Draw graphics on screen
        main.WINDOW.fill(assets.MENU_COLOR)

        title = assets.TITLE_FONT.render('Air Traffic Controller Simulator', True, assets.MENU_TITLE_COLOR)
        main.WINDOW.blit(title, (75, 10))
        main.WINDOW.blit(assets.MENU_IMAGE, (550, 75))

        # Draw buttons
        load_game_button.draw(main.WINDOW)
        load_game_text = assets.BUTTON_FONT.render('Load Game', True, assets.BUTTON_TEXT_COLOR)
        main.WINDOW.blit(load_game_text, (160, 265))

        new_game_button.draw(main.WINDOW)
        new_game_text = assets.BUTTON_FONT.render('New Game', True, assets.BUTTON_TEXT_COLOR)
        main.WINDOW.blit(new_game_text, (160, 365))

        # Run event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.close()

        pygame.display.flip()


# Define buttons
button_width = 200
button_height = 50
button_curve = 10
button_x = 100

load_game_button = graphics.Button(
    button_x,
    250,
    button_width,
    button_height,
    assets.MENU_BUTTON_COLOR,
    assets.MENU_BUTTON_COLOR_OVER,
    assets.MENU_BUTTON_COLOR_DOWN,
    button_curve
)

new_game_button = graphics.Button(
    button_x,
    350,
    button_width,
    button_height,
    assets.MENU_BUTTON_COLOR,
    assets.MENU_BUTTON_COLOR_OVER,
    assets.MENU_BUTTON_COLOR_DOWN,
    button_curve
)
