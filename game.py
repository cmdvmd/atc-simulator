import pygame
import main
import graphics
import assets


def draw_controls():
    """
    Draw controls graphics on screen
    """

    global drawing_runway
    global pressed

    # Define buttons
    button_size = 75
    button_curve = 10
    button_y = main.SCREEN_HEIGHT - button_size - 10

    # Draw runway button
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

    draw_runway_button.draw(main.WINDOW)
    if draw_runway_button.clicked and not pressed:
        drawing_runway = not drawing_runway
        pygame.mouse.set_cursor(*(pygame.cursors.broken_x if drawing_runway else pygame.cursors.arrow))
        pressed = True

    if not drawing_runway:
        top_text_y = button_y + 5
        bottom_text_y = button_y + 25
        price_text_y = button_y + 45

        # Draw runway button
        draw_text = assets.BUTTON_FONT.render('Draw', True, assets.INFO_TEXT_COLOR)
        runway_text = assets.BUTTON_FONT.render('Runway', True, assets.INFO_TEXT_COLOR)
        runway_price_text = assets.BUTTON_FONT.render(f'(${assets.RUNWAY_PRICE:,}/sq. ft)', True,
                                                      assets.INFO_TEXT_COLOR)
        main.WINDOW.blit(draw_text, (32, top_text_y))
        main.WINDOW.blit(runway_text, (25, bottom_text_y))
        main.WINDOW.blit(runway_price_text, (17, price_text_y))

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

        # Draw expand terminal button
        expand_terminal_button.draw(main.WINDOW)

        expand_text = assets.BUTTON_FONT.render('Expand', True, assets.INFO_TEXT_COLOR)
        terminal_text = assets.BUTTON_FONT.render('Terminal', True, assets.INFO_TEXT_COLOR)
        terminal_price_text = assets.BUTTON_FONT.render(f'(${assets.TERMINAL_PRICE:,})', True, assets.INFO_TEXT_COLOR)
        main.WINDOW.blit(expand_text, (110, top_text_y))
        main.WINDOW.blit(terminal_text, (108, bottom_text_y))
        main.WINDOW.blit(terminal_price_text, (102, price_text_y))

        if expand_terminal_button.clicked and main.data[assets.TERMINAL_SIZE] <= 500 and main.data[
            assets.BALANCE] >= assets.TERMINAL_PRICE and not pressed:
            main.data[assets.BALANCE] -= assets.TERMINAL_PRICE
            main.data[assets.TERMINAL_SIZE] += 50
            pressed = True
    else:
        # Draw exit runway button
        exit_button = assets.INFO_FONT.render('Exit', True, assets.INFO_TEXT_COLOR)
        main.WINDOW.blit(exit_button, (33, button_y + 25))


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
    terminal_width = main.data[assets.TERMINAL_SIZE]
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

    top_y = int(terminal_y - gate_height)
    bottom_y = int(terminal_y + terminal_height)

    mouse_pos = pygame.mouse.get_pos()

    for i, x in enumerate(range(int(terminal_x + terminal_curve), int(terminal_x + terminal_width), gate_spacing)):
        # Draw top gate
        pygame.draw.rect(main.WINDOW, assets.GATE_COLOR, pygame.Rect(
            x,
            top_y,
            gate_width,
            gate_height
        ))
        pygame.draw.rect(main.WINDOW, assets.GATE_COLOR, pygame.Rect(
            x,
            top_y,
            gate_arm_length,
            gate_width
        ))

        top_gate = pygame.Rect(x, top_y, gate_arm_length, gate_height)

        # Draw bottom gate
        pygame.draw.rect(main.WINDOW, assets.GATE_COLOR, pygame.Rect(
            x,
            bottom_y,
            gate_width,
            gate_height
        ))
        pygame.draw.rect(main.WINDOW, assets.GATE_COLOR, pygame.Rect(
            x,
            bottom_y + gate_height - gate_width,
            gate_arm_length,
            gate_width
        ))

        bottom_gate = pygame.Rect(x, bottom_y, gate_arm_length, gate_height)

        gates.update({i: x + gate_arm_length})

        if clicked_airplane is not None and clicked_airplane.grounded:
            if top_gate.collidepoint(mouse_pos):
                clicked_airplane.gate_number = i
                clicked_airplane.gate_y = top_y + gate_width - clicked_airplane.grounded_size
                clicked_airplane.gate_angle = 270
                clicked_airplane.gate = True
                clicked_airplane.parked = True
                unclick_airplane()
            elif bottom_gate.collidepoint(mouse_pos):
                clicked_airplane.gate_number = i
                clicked_airplane.gate_y = bottom_y + gate_height - gate_width
                clicked_airplane.gate_angle = 90
                clicked_airplane.gate = True
                clicked_airplane.parked = True
                unclick_airplane()


def draw_runways():
    """
    Draw runways graphics on screen
    """

    mouse_pos = pygame.mouse.get_pos()
    for runway in main.data[assets.RUNWAYS]:
        runway.draw(main.WINDOW)
        collision = runway.collide_end(*mouse_pos)
        if clicked_airplane is not None and collision[1] != -1 and (
                not clicked_airplane.grounded or clicked_airplane.at_gate is not None):
            if collision[0].area >= clicked_airplane.runway_size:
                clicked_airplane.runway = collision[0]
                clicked_airplane.runway_angle = collision[1]
            else:
                clicked_airplane.path.clear()
            unclick_airplane()

    if drawing_runway and original_click is not None:
        runway = graphics.Runway(original_click, pygame.mouse.get_pos())
        runway.draw(main.WINDOW)
        price_text = assets.INFO_FONT.render(f'${runway.price:,}', True,
                                             assets.INFO_ERROR_COLOR if runway.price > main.data[
                                                 assets.BALANCE] else assets.INFO_TEXT_COLOR)
        price_text_rect = price_text.get_rect()
        main.WINDOW.blit(price_text, (runway.x, runway.y - price_text_rect.height))

        image = None
        if runway.area >= assets.LARGE_PLANE_RUNWAY:
            image = assets.LARGE_PLANE
        elif runway.area >= assets.MEDIUM_PLANE_RUNWAY:
            image = assets.MEDIUM_PLANE
        elif runway.area >= assets.SMALL_PLANE_RUNWAY:
            image = assets.SMALL_PLANE

        if image is not None:
            image = pygame.transform.scale(image, (40, 40))
            main.WINDOW.blit(image, (runway.x, runway.y - price_text_rect.height - image.get_rect().height))


def draw_airplanes():
    """
    Draw airplane graphics on screen
    """

    for airplane in main.data[assets.AIRPLANES]:
        for other in main.data[assets.AIRPLANES]:
            if other != airplane and airplane.grounded == other.grounded and airplane.get_rect().colliderect(
                    other.get_rect()):
                airplane.color = assets.INFO_ERROR_COLOR
                other.color = assets.INFO_ERROR_COLOR
                other.draw(main.WINDOW)

        airplane.draw(main.WINDOW)


def unclick_airplane():
    """
    Callback when airplane is no longer clicked
    """

    global clicked_airplane

    if clicked_airplane is not None:
        clicked_airplane.clicked = False
    clicked_airplane = None


def game():
    """
    Run game loop
    """

    global pressed
    global original_click
    global drawing_runway
    global clicked_airplane

    run = True

    # Speed up plane generation
    pygame.time.set_timer(assets.GENERATE_AIRPLANE, 30000)

    while run:
        main.CLOCK.tick(main.FPS)

        # Draw graphics on screen
        main.WINDOW.fill(assets.GRASS_COLOR)
        draw_airport()
        draw_runways()
        draw_airplanes()
        draw_controls()

        balance_text = assets.INFO_FONT.render(f'${main.data[assets.BALANCE]:,}', True, assets.INFO_TEXT_COLOR)
        balance_rect = balance_text.get_rect()
        main.WINDOW.blit(balance_text, (main.SCREEN_WIDTH - balance_rect.width - 10, 10))

        # Run event loop
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                main.close()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT and not drawing_runway:
                    for airplane in main.data[assets.AIRPLANES]:
                        if airplane.get_rect().collidepoint(mouse_pos) and airplane.ready and (
                                airplane.path or (airplane.runway is None and not airplane.parked)):
                            airplane.clicked = True
                            airplane.path.clear()
                            airplane.runway = None
                            airplane.runway_angle = -1
                            airplane.gate_number = None
                            airplane.gate_angle = None
                            airplane.gate = False
                            clicked_airplane = airplane
                elif event.button == pygame.BUTTON_RIGHT:
                    if drawing_runway:
                        for runway in main.data[assets.RUNWAYS]:
                            runway.rect.x = runway.x
                            runway.rect.y = runway.y
                            if runway.rect.collidepoint(mouse_pos):
                                main.data[assets.RUNWAYS].remove(runway)
                                main.data[assets.BALANCE] += runway.price
                    elif clicked_airplane is not None:
                        clicked_airplane.path.clear()
                        unclick_airplane()
                elif drawing_runway:
                    original_click = mouse_pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if drawing_runway and original_click is not None:
                    runway = graphics.Runway(original_click, mouse_pos)
                    runway.draw(main.WINDOW)
                    if runway.price <= main.data[assets.BALANCE]:
                        main.data[assets.RUNWAYS].append(runway)
                        main.data[assets.BALANCE] -= runway.price
                pressed = False
                original_click = None
                unclick_airplane()
            elif event.type == pygame.MOUSEMOTION and clicked_airplane is not None and (
                    not clicked_airplane.path or clicked_airplane.path[-1] != mouse_pos):
                clicked_airplane.path.append(mouse_pos)
            elif event.type == assets.SPEED_GENERATION:
                main.data[assets.TIMEOUT] = (main.data[assets.TIMEOUT] - 2000) if main.data[assets.TIMEOUT] >= 2000 else 0
                pygame.time.set_timer(assets.GENERATE_AIRPLANE, 0)
                pygame.time.set_timer(assets.GENERATE_AIRPLANE, main.data[assets.TIMEOUT])
            elif event.type == assets.GENERATE_AIRPLANE:
                graphics.Airplane.generate_airplane()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
                pygame.time.set_timer(assets.GENERATE_AIRPLANE, 0)
                run = False

        pygame.display.flip()


drawing_runway = False
pressed = False
original_click = None
clicked_airplane = None
gates = {}
