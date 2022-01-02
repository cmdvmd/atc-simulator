import pygame
import time
import datetime
import main
import graphics
import assets


def draw_popup():
    """
    Draw popup at the end of the game
    """

    global run

    popup = pygame.Surface((main.SCREEN_WIDTH / 2, main.SCREEN_HEIGHT / 2), pygame.SRCALPHA)
    popup_center_x = popup.get_width() / 2
    popup_pos = main.SCREEN_CENTER[0] - popup_center_x, main.SCREEN_CENTER[1] - (popup.get_height() / 2)
    popup.fill(assets.POPUP_COLOR)

    title = assets.TITLE_FONT.render('Game Over!', True, assets.MENU_TITLE_COLOR)
    title_y = 10

    score = assets.POPUP_FONT.render(f'Score: {main.data[assets.SCORE]}', True, assets.INFO_TEXT_COLOR)
    score_y = title_y + title.get_height() + 10

    high_score = assets.POPUP_FONT.render(
        f'High Score: {max(main.data[assets.HIGH_SCORE], main.data[assets.SCORE])}' + (
            ' (New)' if main.data[assets.SCORE] > main.data[assets.HIGH_SCORE] else ''), True, assets.INFO_TEXT_COLOR)
    high_score_y = score_y + score.get_height() + 10

    game_time = assets.POPUP_FONT.render(
        f'Game Time: {datetime.timedelta(seconds=main.data[assets.GAME_TIME] // 1000)}', True, assets.INFO_TEXT_COLOR)
    game_time_y = high_score_y + high_score.get_height() + 10

    close_button_width = 100
    close_button_height = 35
    close_button = graphics.Button(
        popup_center_x - (close_button_width / 2),
        popup.get_height() - close_button_height - 10,
        close_button_width,
        close_button_height,
        assets.MENU_BUTTON_COLOR,
        assets.MENU_BUTTON_COLOR_OVER,
        assets.MENU_BUTTON_COLOR_DOWN,
        10
    )

    close_text = assets.BUTTON_FONT.render('Close', True, assets.INFO_TEXT_COLOR)

    popup.blit(title, ((popup_center_x - title.get_width() / 2), title_y))
    popup.blit(score, ((popup_center_x - score.get_width() / 2), score_y))
    popup.blit(high_score, ((popup_center_x - high_score.get_width() / 2), high_score_y))
    popup.blit(game_time, ((popup_center_x - game_time.get_width() / 2), game_time_y))

    close_button.draw(popup, popup_pos)
    popup.blit(close_text, (close_button.x + (close_button.width / 2) - (close_text.get_width() / 2),
                            close_button.y + (close_button.height / 2) - (close_text.get_height() / 2)))

    if close_button.clicked:
        end_loop()

    main.WINDOW.blit(popup, popup_pos)


def draw_controls():
    """
    Draw controls graphics on screen
    """

    global drawing_runway
    global hitboxes
    global pressed

    # Define buttons
    button_size = 75
    button_curve = 10
    button_y = main.SCREEN_HEIGHT - button_size - 10

    draw_runway_x = 10
    draw_runway_center_x = draw_runway_x + (button_size / 2)
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

    expand_terminal_x = draw_runway_x + button_size + 10
    expand_terminal_center_x = expand_terminal_x + (button_size / 2)
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

    hitbox_button_x = expand_terminal_x + button_size + 10
    hitbox_center_x = hitbox_button_x + (button_size / 2)
    hitbox_center_y = button_y + (button_size / 2)
    hitbox_button = graphics.Button(
        hitbox_button_x,
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

    if not drawing_runway:
        top_text_y = button_y + 7
        bottom_text_y = button_y + (button_size / 2) - (assets.BUTTON_FONT.get_height() / 2)
        price_text_y = button_y + button_size - assets.BUTTON_FONT.get_height() - 7

        # Draw runway button
        draw_text = assets.BUTTON_FONT.render('Draw', True, assets.INFO_TEXT_COLOR)
        runway_text = assets.BUTTON_FONT.render('Runway', True, assets.INFO_TEXT_COLOR)
        runway_price_text = assets.BUTTON_FONT.render(f'(${assets.RUNWAY_PRICE:,}/sq. ft)', True,
                                                      assets.INFO_TEXT_COLOR)
        main.WINDOW.blit(draw_text, (draw_runway_center_x - (draw_text.get_width() / 2), top_text_y))
        main.WINDOW.blit(runway_text, (draw_runway_center_x - (runway_text.get_width() / 2), bottom_text_y))
        main.WINDOW.blit(runway_price_text, (draw_runway_center_x - (runway_price_text.get_width() / 2), price_text_y))

        # Draw expand terminal button
        expand_terminal_button.draw(main.WINDOW)

        expand_text = assets.BUTTON_FONT.render('Expand', True, assets.INFO_TEXT_COLOR)
        terminal_text = assets.BUTTON_FONT.render('Terminal', True, assets.INFO_TEXT_COLOR)
        terminal_price_text = assets.BUTTON_FONT.render(f'(${assets.TERMINAL_PRICE:,})', True, assets.INFO_TEXT_COLOR)
        main.WINDOW.blit(expand_text, (expand_terminal_center_x - (expand_text.get_width() / 2), top_text_y))
        main.WINDOW.blit(terminal_text, (expand_terminal_center_x - (terminal_text.get_width() / 2), bottom_text_y))
        main.WINDOW.blit(terminal_price_text,
                         (expand_terminal_center_x - (terminal_price_text.get_width() / 2), price_text_y))

        # Draw show/hide hit boxes button
        hitbox_button.draw(main.WINDOW)

        status_text = assets.BUTTON_FONT.render('Hide' if hitboxes else 'Show', True, assets.INFO_TEXT_COLOR)
        hit_box_text = assets.BUTTON_FONT.render('Hitboxes', True, assets.INFO_TEXT_COLOR)

        main.WINDOW.blit(status_text,
                         (hitbox_center_x - (status_text.get_width() / 2), hitbox_center_y - status_text.get_height()))
        main.WINDOW.blit(hit_box_text, (hitbox_center_x - (hit_box_text.get_width() / 2), hitbox_center_y))

        if expand_terminal_button.clicked and main.data[assets.TERMINAL_SIZE] <= 500 and main.data[
            assets.BALANCE] >= assets.TERMINAL_PRICE and not pressed:
            main.data[assets.BALANCE] -= assets.TERMINAL_PRICE
            main.data[assets.TERMINAL_SIZE] += 50

        if hitbox_button.clicked and not pressed:
            hitboxes = not hitboxes
    else:
        # Draw exit runway button
        exit_text = assets.INFO_FONT.render('Exit', True, assets.INFO_TEXT_COLOR)
        main.WINDOW.blit(exit_text, (draw_runway_center_x - (exit_text.get_width() / 2),
                                     button_y + (button_size / 2) - (exit_text.get_height() / 2)))

    pressed = draw_runway_button.clicked or expand_terminal_button.clicked or hitbox_button.clicked


def draw_airport():
    """
    Draw airport graphics on screen
    """

    # Draw apron
    apron_width = 600
    apron_height = 250
    apron_curve = 10

    pygame.draw.rect(main.WINDOW, assets.ROAD_COLOR, pygame.Rect(
        main.SCREEN_CENTER[0] - (apron_width / 2),
        main.SCREEN_CENTER[1] - (apron_height / 2),
        apron_width,
        apron_height
    ), border_radius=apron_curve)

    # Draw terminal
    terminal_width = main.data[assets.TERMINAL_SIZE]
    terminal_height = 75
    terminal_x = main.SCREEN_CENTER[0] - (terminal_width / 2)
    terminal_y = main.SCREEN_CENTER[1] - (terminal_height / 2)
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
        result = runway.collide_end(*mouse_pos)
        if clicked_airplane is not None and result[1] != -1 and (
                not clicked_airplane.grounded or clicked_airplane.at_gate is not None):
            if result[0].area >= clicked_airplane.runway_size:
                clicked_airplane.runway = result[0]
                clicked_airplane.runway_angle = result[1]
            else:
                clicked_airplane.path.clear()
            unclick_airplane()

    if drawing_runway and original_click is not None:
        runway = graphics.Runway(original_click, pygame.mouse.get_pos())
        runway.draw(main.WINDOW)
        price_text = assets.INFO_FONT.render(f'${runway.price:,}', True,
                                             assets.INFO_ERROR_COLOR if runway.price > main.data[
                                                 assets.BALANCE] else assets.INFO_TEXT_COLOR)
        main.WINDOW.blit(price_text, (runway.x, runway.y - price_text.get_height()))

        image = None
        if runway.area >= assets.LARGE_PLANE_RUNWAY:
            image = assets.LARGE_PLANE
        elif runway.area >= assets.MEDIUM_PLANE_RUNWAY:
            image = assets.MEDIUM_PLANE
        elif runway.area >= assets.SMALL_PLANE_RUNWAY:
            image = assets.SMALL_PLANE

        if image is not None:
            image = pygame.transform.scale(pygame.image.fromstring(image, assets.PLANE_SIZE, 'RGBA'), (40, 40))
            main.WINDOW.blit(image, (runway.x, runway.y - price_text.get_height() - image.get_height()))


def draw_airplanes():
    """
    Draw airplane graphics on screen
    """

    for airplane in main.data[assets.AIRPLANES]:
        airplane.draw(main.WINDOW)
        for other in main.data[assets.AIRPLANES]:
            if not main.data[
                assets.GAME_OVER] and other != airplane and airplane.grounded == other.grounded and airplane.get_rect().colliderect(
                    other.get_rect()):
                main.data[assets.GAME_TIME] = main.get_time()
                main.data[assets.GAME_OVER] = True
                airplane.color = assets.AIRPLANE_COLLISION_COLOR
                other.color = assets.AIRPLANE_COLLISION_COLOR
                other.draw(main.WINDOW)


def unclick_airplane():
    """
    Callback when airplane is no longer clicked
    """

    global clicked_airplane

    if clicked_airplane is not None:
        clicked_airplane.clicked = False
    clicked_airplane = None


def end_loop():
    global run

    main.save_game()
    main.game_start_time = 0
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    pygame.time.set_timer(assets.SPEED_GENERATION, 0)
    pygame.time.set_timer(assets.GENERATE_AIRPLANE, 0)
    run = False


def game():
    """
    Run game loop
    """

    global run
    global pressed
    global original_click
    global drawing_runway
    global clicked_airplane

    run = True
    main.game_start_time = time.time_ns()

    # Configure plane generation
    pygame.time.set_timer(assets.GENERATE_AIRPLANE, main.data[assets.TIMEOUT])
    pygame.time.set_timer(assets.SPEED_GENERATION, 30000)

    while run:
        main.CLOCK.tick(main.FPS)

        # Draw graphics on screen
        main.WINDOW.fill(assets.GRASS_COLOR)
        draw_airport()
        draw_runways()
        draw_airplanes()
        draw_controls()
        if main.data[assets.GAME_OVER]:
            draw_popup()

        balance_text = assets.INFO_FONT.render(
            ('- ' if main.data[assets.BALANCE] < 0 else '') + f'${abs(main.data[assets.BALANCE]):,}', True,
            assets.INFO_TEXT_COLOR if main.data[assets.BALANCE] >= 0 else assets.INFO_ERROR_COLOR)
        main.WINDOW.blit(balance_text, (main.SCREEN_WIDTH - balance_text.get_width() - 10, 10))

        # Run event loop
        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False
                main.close()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT and not drawing_runway:
                    for airplane in main.data[assets.AIRPLANES]:
                        if airplane.get_rect().collidepoint(mouse_pos) and airplane.ready and (
                                airplane.path or (airplane.runway is None and not airplane.parked)):
                            airplane.clicked = True
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
                        clicked_airplane.parked = False
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
                main.data[assets.TIMEOUT] = (main.data[assets.TIMEOUT] - 2000) if main.data[
                                                                                      assets.TIMEOUT] >= 2000 else 0
                pygame.time.set_timer(assets.GENERATE_AIRPLANE, 0)
                pygame.time.set_timer(assets.GENERATE_AIRPLANE, main.data[assets.TIMEOUT])
            elif event.type == assets.GENERATE_AIRPLANE:
                graphics.Airplane.generate_airplane()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                end_loop()

        pygame.display.flip()


# Define variables
run = False
drawing_runway = False
hitboxes = False
pressed = False
original_click = None
clicked_airplane = None
gates = {}
