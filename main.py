import sys

# بررسی نصب بودن Pygame
try:
    import pygame

except ImportError:
    print("کتابخانه pygame نصب نیست.")
    print("برای نصب این دستور را اجرا کنید: pip install pygame")
    sys.exit(1)


from settings import WIDTH, HEIGHT, FPS
from game_state import new_game, finish_test
from typing_logic import get_elapsed
from ui import (
    make_fonts,
    draw_start_screen,
    draw_typing_screen,
    draw_result_screen
)
from events import handle_events


def main():
    """تابع اصلی برنامه و حلقه اجرای بازی."""

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption(
        "Typing Speed Test - Ten Finger Typing"
    )

    clock = pygame.time.Clock()

    fonts = make_fonts()
    game = new_game()

    running = True

    
    while running:

        mouse_pos = pygame.mouse.get_pos()

        
        running = handle_events(game, fonts)

        
        if (
            game["screen"] == "typing"
            and game["started"]
            and get_elapsed(game) >= game["time_limit"]
        ):
            finish_test(game)

        # مرحله سوم: رسم صفحه مناسب
        if game["screen"] == "start":

            draw_start_screen(
                screen, game, fonts, mouse_pos
            )

        elif game["screen"] == "typing":

            draw_typing_screen(
                screen, game, fonts
            )

        else:

            draw_result_screen(
                screen, game, fonts, mouse_pos
            )

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":

    try:
        main()

    except Exception as error:
        pygame.quit()
        print("خطای غیرمنتظره در برنامه:", error)
        raise