import pygame
import main
import graphics
import assets


def draw_controls():
    """
    Draw controls graphics on screen
    """

    top_text_y = button_y + 15
    bottom_text_y = button_y + 40

    # Draw runway button
    draw_runway_button.draw(main.WINDOW)

    draw_text = assets.BUTTON_FONT.render('Draw', True, assets.BUTTON_TEXT_COLOR)
    runway_text = assets.BUTTON_FONT.render('Runway', True, assets.BUTTON_TEXT_COLOR)
    main.WINDOW.blit(draw_text, (30, top_text_y))
    main.WINDOW.blit(runway_text, (20, bottom_text_y))

    # Draw expand terminal button
    expand_terminal_button.draw(main.WINDOW)

    expand_text = assets.BUTTON_FONT.render('Expand', True, assets.BUTTON_TEXT_COLOR)
    terminal_text = assets.BUTTON_FONT.render('Terminal', True, assets.BUTTON_TEXT_COLOR)
    main.WINDOW.blit(expand_text, (105, top_text_y))
    main.WINDOW.blit(terminal_text, (100, bottom_text_y))


def draw_airport():
    """
    Draw airport graphics on screen
    """

    # Draw apron
    apron_width = 600
    apron_height = 250
    apron_curve = 10

    pygame.draw.rect(main.WINDOW, assets.ROAD_COLOR, pygame.Rect(
        (main.SCREEN_WIDTH / 2) - (apron_width / 2),
        (main.SCREEN_HEIGHT / 2) - (apron_height / 2),
        apron_width,
        apron_height
    ), border_radius=apron_curve)

    # Draw terminal
    terminal_width = 150
    terminal_height = 75
    terminal_x = (main.SCREEN_WIDTH / 2) - (terminal_width / 2)
    terminal_y = (main.SCREEN_HEIGHT / 2) - (terminal_height / 2)
    terminal_curve = 10

    pygame.draw.rect(main.WINDOW, assets.TERMINAL_COLOR, pygame.Rect(
        terminal_x,
        terminal_y,
        terminal_width,
        terminal_height
    ), border_radius=terminal_curve)

    # Draw gates along terminal
    gate_width = 10
    gate_height = 20
    gate_arm_length = 15
    gate_spacing = 50

    for x in range(int(terminal_x + terminal_curve), int(terminal_x + terminal_width), gate_spacing):
        # Draw top gate
        pygame.draw.rect(main.WINDOW, assets.GATE_COLOR, pygame.Rect(
            x,
            terminal_y - gate_height,
            gate_width,
            gate_height
        ))
        pygame.draw.rect(main.WINDOW, assets.GATE_COLOR, pygame.Rect(
            x,
            terminal_y - gate_height,
            gate_arm_length,
            gate_width
        ))

        # Draw bottom gate
        pygame.draw.rect(main.WINDOW, assets.GATE_COLOR, pygame.Rect(
            x,
            terminal_y + terminal_height,
            gate_width,
            gate_height
        ))
        pygame.draw.rect(main.WINDOW, assets.GATE_COLOR, pygame.Rect(
            x,
            terminal_y + terminal_height + gate_height - gate_width,
            gate_arm_length,
            gate_width
        ))


def game():
    """
    Run game loop
    """

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(main.FPS)

        # Draw graphics on screen
        main.WINDOW.fill(assets.GRASS_COLOR)
        draw_controls()
        draw_airport()

        # Run event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main.close()

        pygame.display.flip()


# Define buttons
button_size = 75
button_curve = 10
button_y = main.SCREEN_HEIGHT - button_size - 10

draw_runway_x = 10
draw_runway_button = graphics.Button(
    draw_runway_x,
    button_y,
    button_size,
    button_size,
    assets.BUTTON_COLOR,
    assets.BUTTON_COLOR_OVER,
    assets.BUTTON_COLOR_DOWN,
    button_curve
)

expand_terminal_x = (draw_runway_x * 2) + button_size
expand_terminal_button = graphics.Button(
    expand_terminal_x,
    button_y,
    button_size,
    button_size,
    assets.BUTTON_COLOR,
    assets.BUTTON_COLOR_OVER,
    assets.BUTTON_COLOR_DOWN,
    button_curve
)
