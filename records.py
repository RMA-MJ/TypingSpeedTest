import json

from settings import LEVEL_ORDER, RECORDS_FILE


def default_records():
    """ساخت رکورد اولیه برای تمام سطوح."""
    return {
        key: {"wpm": 0.0, "accuracy": 0.0}
        for key in LEVEL_ORDER
    }


def load_records():
    """خواندن رکوردها از فایل JSON."""
    records = default_records()

    try:
        with open(RECORDS_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        for key in LEVEL_ORDER:
            if key in data:
                records[key]["wpm"] = float(
                    data[key].get("wpm", 0)
                )
                records[key]["accuracy"] = float(
                    data[key].get("accuracy", 0)
                )

    except FileNotFoundError:
        
        pass

    except (ValueError, TypeError, AttributeError, OSError):
        print("Warning: Records file is damaged. Starting with empty records.")
        records = default_records()

    return records


def save_records(records):
    """ذخیره رکوردها در فایل JSON."""
    try:
        with open(RECORDS_FILE, "w", encoding="utf-8") as file:
            json.dump(records, file, indent=2)

    except OSError:
        print("Warning: Could not save records.")