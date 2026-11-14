import pygame

from settings import (
    WIDTH, HEIGHT,
    BG, PANEL, TEXT_BOX, WHITE, MUTED,
    UNTYPED, GREEN, RED, RED_BG, BLUE, YELLOW,
    LEVELS, LEVEL_ORDER,
    LEVEL_RECTS, START_RECT, AGAIN_RECT,
    MENU_RECT, TEXT_RECT
)

from typing_logic import (
    compute_stats,
    get_elapsed,
    rating_message
)


def draw_text(surface, text, font, color, x, y, align="left"):
    """رسم متن با تراز دلخواه."""

    img = font.render(text, True, color)
    rect = img.get_rect()

    if align == "center":
        rect.midtop = (x, y)
    elif align == "right":
        rect.topright = (x, y)
    else:
        rect.topleft = (x, y)

    surface.blit(img, rect)


def draw_button(
    surface, rect, text, font,
    color, mouse_pos, selected=False
):
    """رسم دکمه با افکت قرار گرفتن ماوس روی آن."""

    hover = rect.collidepoint(mouse_pos)

    shade = (
        tuple(min(255, c + 25) for c in color)
        if hover else color
    )

    pygame.draw.rect(
        surface,
        shade,
        rect,
        border_radius=14
    )

    if selected:
        pygame.draw.rect(
            surface,
            WHITE,
            rect,
            width=4,
            border_radius=14
        )

    img = font.render(text, True, WHITE)
    surface.blit(img, img.get_rect(center=rect.center))


def draw_stat_card(surface, fonts, x, label, value, color, y=85):
    """رسم کارت نمایش آمار."""

    rect = pygame.Rect(x, y, 200, 90)

    pygame.draw.rect(
        surface,
        PANEL,
        rect,
        border_radius=14
    )

    draw_text(
        surface, label, fonts["small"],
        MUTED, rect.centerx, rect.y + 10, "center"
    )

    draw_text(
        surface, value, fonts["big"],
        color, rect.centerx, rect.y + 38, "center"
    )


def draw_start_screen(surface, game, fonts, mouse_pos):
    """رسم صفحه شروع برنامه."""

    surface.fill(BG)

    draw_text(
        surface, "Typing Speed Test",
        fonts["title"], YELLOW,
        WIDTH // 2, 50, "center"
    )

    draw_text(
        surface, "Ten Finger Typing",
        fonts["medium"], WHITE,
        WIDTH // 2, 125, "center"
    )

    draw_text(
        surface,
        "Tip: put your fingers on the home row  A S D F   J K L ;",
        fonts["small"], MUTED,
        WIDTH // 2, 185, "center"
    )

    draw_text(
        surface, "Choose your level:",
        fonts["medium"], WHITE,
        WIDTH // 2, 250, "center"
    )

    for key in LEVEL_ORDER:
        draw_button(
            surface,
            LEVEL_RECTS[key],
            LEVELS[key]["label"],
            fonts["medium"],
            LEVELS[key]["color"],
            mouse_pos,
            selected=(key == game["level"])
        )

    draw_button(
        surface, START_RECT, "START",
        fonts["big"], BLUE, mouse_pos
    )

    draw_text(
        surface, "or press ENTER",
        fonts["small"], MUTED,
        WIDTH // 2, 475, "center"
    )

    
    panel = pygame.Rect(150, 515, 700, 105)

    pygame.draw.rect(
        surface, PANEL, panel, border_radius=14
    )

    draw_text(
        surface, "Best Records",
        fonts["small"], YELLOW,
        WIDTH // 2, panel.y + 8, "center"
    )

    for i, key in enumerate(LEVEL_ORDER):
        rec = game["records"][key]
        cx = panel.x + 120 + i * 230

        draw_text(
            surface,
            LEVELS[key]["label"],
            fonts["small"],
            LEVELS[key]["color"],
            cx, panel.y + 38, "center"
        )

        if rec["wpm"] > 0:
            info = (
                f"{rec['wpm']:.1f} WPM  |  "
                f"{rec['accuracy']:.0f}%"
            )
        else:
            info = "No record yet"

        draw_text(
            surface, info, fonts["small"],
            WHITE, cx, panel.y + 66, "center"
        )


def draw_typing_screen(surface, game, fonts):
    """رسم صفحه اصلی تایپ."""

    surface.fill(BG)

    level = LEVELS[game["level"]]
    elapsed = get_elapsed(game)

    remaining = max(
        0.0,
        game["time_limit"] - elapsed
    )

    stats = compute_stats(
        game["target"],
        game["typed"],
        elapsed
    )

    draw_text(
        surface,
        f"Level: {level['label']}",
        fonts["medium"],
        level["color"],
        60, 30
    )

    draw_text(
        surface,
        "ESC = menu     TAB = restart",
        fonts["small"],
        MUTED,
        WIDTH - 60, 40, "right"
    )

    live_wpm = stats["wpm"] if elapsed >= 2 else 0.0

    time_color = (
        RED
        if remaining <= 10 and game["started"]
        else WHITE
    )

    draw_stat_card(
        surface, fonts, 61,
        "TIME LEFT", f"{remaining:.1f}s",
        time_color
    )

    draw_stat_card(
        surface, fonts, 287,
        "SPEED (WPM)", f"{live_wpm:.0f}",
        YELLOW
    )

    draw_stat_card(
        surface, fonts, 513,
        "ACCURACY",
        f"{stats['accuracy']:.0f}%" if game["typed"] else "--",
        GREEN
    )

    draw_stat_card(
        surface, fonts, 739,
        "MISTAKES", str(stats["errors"]),
        RED
    )

    pygame.draw.rect(
        surface, TEXT_BOX,
        TEXT_RECT, border_radius=16
    )

    mono = fonts["mono"]
    char_h = mono.get_linesize()
    typed = game["typed"]

    for i, ch in enumerate(game["target"]):
        x, y = game["layout"][i]
        char_w = mono.size(ch)[0]

        if i < len(typed):
            if typed[i] == ch:
                color = GREEN
            else:
                color = RED

                pygame.draw.rect(
                    surface,
                    RED_BG,
                    (x, y, char_w, char_h)
                )
        else:
            color = UNTYPED

        surface.blit(
            mono.render(ch, True, color),
            (x, y)
        )

        if i == len(typed):
            pygame.draw.rect(
                surface,
                BLUE,
                (x, y + char_h, char_w, 4)
            )

    bar = pygame.Rect(60, 480, 880, 14)

    pygame.draw.rect(
        surface, PANEL, bar, border_radius=7
    )

    progress = (
        len(typed) / len(game["target"])
        if game["target"] else 0
    )

    fill = pygame.Rect(
        bar.x,
        bar.y,
        int(bar.width * progress),
        bar.height
    )

    pygame.draw.rect(
        surface, BLUE, fill, border_radius=7
    )

    if not game["started"]:
        draw_text(
            surface,
            "Start typing to begin the timer...",
            fonts["medium"], YELLOW,
            WIDTH // 2, 520, "center"
        )

    elif len(typed) < len(game["target"]):
        nxt = game["target"][len(typed)]
        name = "SPACE" if nxt == " " else nxt

        draw_text(
            surface,
            f"Next key:  {name}",
            fonts["medium"], WHITE,
            WIDTH // 2, 520, "center"
        )

    draw_text(
        surface,
        "Use BACKSPACE to fix a mistake. Use all ten fingers!",
        fonts["small"], MUTED,
        WIDTH // 2, 600, "center"
    )


def draw_result_screen(surface, game, fonts, mouse_pos):
    """رسم صفحه نتیجه آزمون."""

    surface.fill(BG)

    res = game["results"]
    level = LEVELS[game["level"]]

    draw_text(
        surface, "Test Finished!",
        fonts["title"], YELLOW,
        WIDTH // 2, 20, "center"
    )

    draw_text(
        surface,
        f"Level: {level['label']}",
        fonts["medium"],
        level["color"],
        WIDTH // 2, 100, "center"
    )

    items = [
        ("SPEED (WPM)", f"{res['wpm']:.1f}", YELLOW),
        ("ACCURACY", f"{res['accuracy']:.1f}%", GREEN),
        ("MISTAKES", str(res["errors"]), RED),
        ("TIME", f"{res['elapsed']:.1f}s", WHITE),
    ]

    for i, (label, value, color) in enumerate(items):
        draw_stat_card(
            surface,
            fonts,
            61 + i * 226,
            label,
            value,
            color,
            y=145
        )

    draw_text(
        surface,
        f"Characters typed: {res['typed_count']} "
        f"of {len(game['target'])}   |   "
        f"Correct: {res['correct']}",
        fonts["small"], MUTED,
        WIDTH // 2, 248, "center"
    )

    if game["new_record"]:
        draw_text(
            surface, "NEW RECORD!",
            fonts["big"], YELLOW,
            WIDTH // 2, 282, "center"
        )

    elif res["typed_count"] == 0:
        draw_text(
            surface,
            "You did not type anything. Try again!",
            fonts["medium"], WHITE,
            WIDTH // 2, 285, "center"
        )

    else:
        draw_text(
            surface,
            rating_message(res["wpm"]),
            fonts["medium"], WHITE,
            WIDTH // 2, 285, "center"
        )

    best = game["records"][game["level"]]

    panel = pygame.Rect(250, 350, 500, 140)

    pygame.draw.rect(
        surface, PANEL, panel, border_radius=14
    )

    draw_text(
        surface,
        f"Best record ({level['label']})",
        fonts["medium"], YELLOW,
        WIDTH // 2, panel.y + 18, "center"
    )

    if best["wpm"] > 0:
        info = (
            f"{best['wpm']:.1f} WPM   |   "
            f"{best['accuracy']:.1f}% accuracy"
        )
    else:
        info = "No record yet"

    draw_text(
        surface, info, fonts["medium"],
        WHITE, WIDTH // 2, panel.y + 70, "center"
    )

    draw_button(
        surface, AGAIN_RECT,
        "Try Again", fonts["medium"],
        BLUE, mouse_pos
    )

    draw_button(
        surface, MENU_RECT,
        "Main Menu", fonts["medium"],
        (100, 116, 160), mouse_pos
    )

    draw_text(
        surface,
        "ENTER = try again     ESC = menu",
        fonts["small"], MUTED,
        WIDTH // 2, 615, "center"
    )


def make_fonts():
    """ساخت فونت‌های رابط کاربری و متن تایپ."""

    ui = "arial,helvetica,dejavusans,liberationsans"

    mono = (
        "consolas,couriernew,dejavusansmono,"
        "liberationmono,menlo,monospace"
    )

    try:
        return {
            "title": pygame.font.SysFont(ui, 64, bold=True),
            "big": pygame.font.SysFont(ui, 38, bold=True),
            "medium": pygame.font.SysFont(ui, 28, bold=True),
            "small": pygame.font.SysFont(ui, 20),
            "mono": pygame.font.SysFont(mono, 30, bold=True),
        }

    except Exception:
        return {
            "title": pygame.font.Font(None, 72),
            "big": pygame.font.Font(None, 44),
            "medium": pygame.font.Font(None, 32),
            "small": pygame.font.Font(None, 24),
            "mono": pygame.font.Font(None, 34),
        }