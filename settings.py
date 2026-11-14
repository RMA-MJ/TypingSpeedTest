import pygame

WIDTH, HEIGHT = 1000, 650
FPS = 60

# رنگ‌ها
BG = (24, 31, 66)
PANEL = (40, 52, 102)
TEXT_BOX = (250, 247, 235)
WHITE = (255, 255, 255)
MUTED = (160, 170, 205)
UNTYPED = (110, 110, 125)
GREEN = (22, 163, 74)
RED = (220, 38, 38)
RED_BG = (254, 205, 205)
BLUE = (59, 130, 246)
YELLOW = (255, 200, 60)


LEVELS = {
    "easy": {
        "label": "Easy",
        "time": 60,
        "color": (34, 197, 94),
        "texts": [
            "the sun is bright and the sky is blue today",
            "i like to read books in the school library",
            "my cat sleeps on the soft green sofa all day",
            "we play football with our friends after class",
            "a good student practices a little every day",
        ],
    },
    "medium": {
        "label": "Medium",
        "time": 50,
        "color": (245, 158, 11),
        "texts": [
            "Typing with ten fingers helps you write faster, and it saves a lot of time.",
            "Our teacher said that practice makes perfect, so we practice every single day.",
            "The quick brown fox jumps over the lazy dog near the old wooden bridge.",
            "Keep your fingers on the home row and try not to look at the keyboard.",
        ],
    },
    "hard": {
        "label": "Hard",
        "time": 50,
        "color": (239, 68, 68),
        "texts": [
            "On 15 May 2025, the team solved 42 problems in just 7 minutes; amazing, isn't it?",
            "Python's print() function shows text: print(\"Hello, World!\") is the first program.",
            "Dr. Smith's lab (room #305) opened at 8:30 a.m. and closed at 5:45 p.m. on 12/09.",
            "Accuracy matters more than speed; typing fast with 20% mistakes is really slow!",
        ],
    },
}

LEVEL_ORDER = ["easy", "medium", "hard"]

import os

RECORDS_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "best_records.json"
)

LEVEL_RECTS = {
    key: pygame.Rect(150 + i * 250, 300, 200, 60)
    for i, key in enumerate(LEVEL_ORDER)
}

START_RECT = pygame.Rect(350, 395, 300, 70)
AGAIN_RECT = pygame.Rect(230, 545, 240, 60)
MENU_RECT = pygame.Rect(530, 545, 240, 60)
TEXT_RECT = pygame.Rect(60, 210, 880, 250)