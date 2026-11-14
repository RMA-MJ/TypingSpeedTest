import time
import pygame

from settings import (
    LEVEL_ORDER,
    LEVEL_RECTS,
    START_RECT,
    AGAIN_RECT,
    MENU_RECT
)

from game_state import start_test, finish_test


def handle_events(game, fonts):
    """مدیریت رویدادهای کیبورد، ماوس و بستن پنجره."""

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            return False

        screen = game["screen"]

        # صفحه شروع
        if screen == "start":

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                for key in LEVEL_ORDER:
                    if LEVEL_RECTS[key].collidepoint(event.pos):
                        game["level"] = key

                if START_RECT.collidepoint(event.pos):
                    start_test(game, fonts)

            elif event.type == pygame.KEYDOWN:

                if event.key in (
                    pygame.K_RETURN,
                    pygame.K_KP_ENTER
                ):
                    start_test(game, fonts)

                elif event.key == pygame.K_1:
                    game["level"] = "easy"

                elif event.key == pygame.K_2:
                    game["level"] = "medium"

                elif event.key == pygame.K_3:
                    game["level"] = "hard"

                elif event.key == pygame.K_ESCAPE:
                    return False

        # صفحه تایپ
        elif screen == "typing":

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    game["screen"] = "start"

                elif event.key == pygame.K_TAB:
                    start_test(game, fonts)

                elif event.key == pygame.K_BACKSPACE:
                    game["typed"] = game["typed"][:-1]

                else:
                    ch = event.unicode

                    if (
                        ch
                        and ch.isprintable()
                        and len(game["typed"]) < len(game["target"])
                    ):

                        if not game["started"]:
                            game["started"] = True
                            game["start_time"] = time.time()

                        game["typed"] += ch

                        if len(game["typed"]) == len(game["target"]):
                            finish_test(game)

        # صفحه نتیجه
        elif screen == "result":

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                if AGAIN_RECT.collidepoint(event.pos):
                    start_test(game, fonts)

                elif MENU_RECT.collidepoint(event.pos):
                    game["screen"] = "start"

            elif event.type == pygame.KEYDOWN:

                if event.key in (
                    pygame.K_RETURN,
                    pygame.K_KP_ENTER
                ):
                    start_test(game, fonts)

                elif event.key == pygame.K_ESCAPE:
                    game["screen"] = "start"

    return True