import random
import time

from settings import LEVELS
from records import load_records, save_records
from text_layout import build_layout
from typing_logic import compute_stats, get_elapsed


def new_game():
    """ساخت وضعیت اولیه برنامه."""

    return {
        "screen": "start",
        "level": "easy",
        "target": "",
        "typed": "",
        "layout": [],
        "started": False,
        "finished": False,
        "start_time": 0.0,
        "end_time": 0.0,
        "time_limit": 60,
        "results": None,
        "new_record": False,
        "records": load_records(),
    }


def start_test(game, fonts):
    """شروع آزمون جدید با انتخاب متن تصادفی."""

    level = LEVELS[game["level"]]

    game["target"] = random.choice(level["texts"])
    game["layout"] = build_layout(
        game["target"],
        fonts["mono"]
    )

    game["typed"] = ""
    game["started"] = False
    game["finished"] = False
    game["start_time"] = 0.0
    game["end_time"] = 0.0
    game["time_limit"] = level["time"]
    game["results"] = None
    game["new_record"] = False
    game["screen"] = "typing"


def finish_test(game):
    """پایان آزمون، محاسبه نتیجه و بررسی رکورد جدید."""

    if game["finished"]:
        return

    game["finished"] = True

    if game["started"]:
        game["end_time"] = min(
            time.time(),
            game["start_time"] + game["time_limit"]
        )

    elapsed = get_elapsed(game)

    results = compute_stats(
        game["target"],
        game["typed"],
        elapsed
    )

    results["elapsed"] = elapsed
    results["typed_count"] = len(game["typed"])

    game["results"] = results

    best = game["records"][game["level"]]

    if (
        results["typed_count"] > 0
        and results["wpm"] > best["wpm"]
    ):
        best["wpm"] = results["wpm"]
        best["accuracy"] = results["accuracy"]

        game["new_record"] = True
        save_records(game["records"])

    game["screen"] = "result"