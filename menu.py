import pygame
import pickle
import assets
import main
import graphics
import game


def load_game():
    try:
        with open(assets.SAVE_FILE, 'rb') as file:
            main.data = pickle.load(file)
        game.game()
    except (FileNotFoundError, pickle.UnpicklingError):
        return


def new_game():
    main.data = {
        assets.BALANCE: 5000000,
        assets.TERMINAL_SIZE: 150,
        assets.RUNWAYS: [],
        assets.AIRPLANES: [],
        assets.TIMEOUT: 30000,
        assets.TICKS: pygame.time.get_ticks()
    }
    game.game()


def menu():
    """
    Run main menu loop
    """

    run = True

    while run:
        main.CLOCK.tick(main.FPS)

        # Draw graphics on screen
        main.WINDOW.fill(assets.MENU_COLOR)

        title = assets.TITLE_FONT.render('Air Traffic Controller Simulator', True, assets.MENU_TITLE_COLOR)
        main.WINDOW.blit(title, (75, 10))
        main.WINDOW.blit(assets.MENU_IMAGE, (550, 75))

        # Draw buttons
        rules_button.draw(main.WINDOW)
        rules_text = assets.INFO_FONT.render('Rules', True, assets.INFO_TEXT_COLOR)
        main.WINDOW.blit(rules_text, (180, 215))

        load_game_button.draw(main.WINDOW)
        load_game_text = assets.INFO_FONT.render('Load Game', True, assets.INFO_TEXT_COLOR)
        main.WINDOW.blit(load_game_text, (160, 315))

        new_game_button.draw(main.WINDOW)
        new_game_text = assets.INFO_FONT.render('New Game', True, assets.INFO_TEXT_COLOR)
        main.WINDOW.blit(new_game_text, (160, 415))

        if load_game_button.clicked:
            load_game()
            load_game_button.clicked = False
        if new_game_button.clicked:
            new_game()
            new_game_button.clicked = False

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

rules_button = graphics.Button(
    button_x,
    200,
    button_width,
    button_height,
    assets.MENU_BUTTON_COLOR,
    assets.MENU_BUTTON_COLOR_OVER,
    assets.MENU_BUTTON_COLOR_DOWN,
    button_curve
)

load_game_button = graphics.Button(
    button_x,
    300,
    button_width,
    button_height,
    assets.MENU_BUTTON_COLOR,
    assets.MENU_BUTTON_COLOR_OVER,
    assets.MENU_BUTTON_COLOR_DOWN,
    button_curve
)

new_game_button = graphics.Button(
    button_x,
    400,
    button_width,
    button_height,
    assets.MENU_BUTTON_COLOR,
    assets.MENU_BUTTON_COLOR_OVER,
    assets.MENU_BUTTON_COLOR_DOWN,
    button_curve
)
