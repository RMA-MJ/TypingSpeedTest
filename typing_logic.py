import time


def compute_stats(target, typed, elapsed):
    """محاسبه تعداد حروف درست، خطاها، دقت و سرعت تایپ."""

    correct = sum(
        1 for a, b in zip(target, typed)
        if a == b
    )

    total = len(typed)
    errors = total - correct

    accuracy = (
        correct / total * 100
        if total > 0 else 0.0
    )

    if elapsed > 0:
        wpm = (correct / 5) / (max(elapsed, 1.0) / 60)
    else:
        wpm = 0.0

    return {
        "correct": correct,
        "errors": errors,
        "accuracy": accuracy,
        "wpm": wpm,
    }


def get_elapsed(game):
    """محاسبه زمان سپری‌شده از شروع آزمون."""

    if not game["started"]:
        return 0.0

    if game["finished"]:
        return game["end_time"] - game["start_time"]

    return time.time() - game["start_time"]


def rating_message(wpm):
    """تولید پیام متناسب با سرعت تایپ."""

    if wpm < 15:
        return "Good start! Keep practicing every day."

    if wpm < 30:
        return "Nice work! You are getting faster."

    if wpm < 50:
        return "Great job! Your typing is above average."

    return "Excellent! You type like a pro!"