import pygame
import pickle
import assets
import main
import graphics
import instructions
import game


def load_game(start=True):
    """
    Load game data from savefile
    """

    try:
        with open(assets.SAVE_FILE, 'rb') as file:
            main.data = pickle.load(file)
        assert list(main.data.keys()) == assets.DATA_KEYS
    except (FileNotFoundError, AssertionError, pickle.UnpicklingError):
        return
    else:
        if start:
            game.game()


def new_game():
    """
    Reset game data
    """

    load_game(False)
    main.data = {
        assets.BALANCE: 5000000,
        assets.TERMINAL_SIZE: 150,
        assets.RUNWAYS: [],
        assets.AIRPLANES: [],
        assets.TIMEOUT: 32000,
        assets.GAME_TIME: 0,
        assets.SCORE: 0,
        assets.HIGH_SCORE: main.data[assets.HIGH_SCORE] if assets.HIGH_SCORE in main.data else 0,
        assets.GAME_OVER: False
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
        main.WINDOW.blit(title, ((main.SCREEN_WIDTH / 2) - (title.get_width() / 2), 10))
        main.WINDOW.blit(assets.MENU_IMAGE, (550, 75))

        # Draw buttons
        instructions_button.draw(main.WINDOW)
        instructions_text = assets.INFO_FONT.render('Instructions', True, assets.INFO_TEXT_COLOR)
        main.WINDOW.blit(instructions_text, (instructions_button.x + (button_width / 2) - (instructions_text.get_width() / 2), 215))

        load_game_button.draw(main.WINDOW)
        load_game_text = assets.INFO_FONT.render('Load Game', True, assets.INFO_TEXT_COLOR)
        main.WINDOW.blit(load_game_text, (load_game_button.x + (button_width / 2) - (load_game_text.get_width() / 2), 315))

        new_game_button.draw(main.WINDOW)
        new_game_text = assets.INFO_FONT.render('New Game', True, assets.INFO_TEXT_COLOR)
        main.WINDOW.blit(new_game_text, (new_game_button.x + (button_width / 2) - (new_game_text.get_width() / 2), 415))

        if instructions_button.clicked:
            instructions.instructions()
            instructions_button.clicked = False
        if load_game_button.clicked:
            load_game()
            load_game_button.clicked = False
        if new_game_button.clicked:
            new_game()
            new_game_button.clicked = False

        # Run event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                main.close()

        pygame.display.flip()


# Define buttons
button_width = 200
button_height = 50
button_curve = 10
button_x = 100

instructions_button = graphics.Button(
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
