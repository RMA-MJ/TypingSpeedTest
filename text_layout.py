from settings import TEXT_RECT


def wrap_text(text, font, max_width):
    """شکستن متن به چند خط با حفظ فاصله‌های اصلی."""

    words = text.split(" ")
    lines = []
    current = ""

    for i, word in enumerate(words):
        piece = word + (" " if i < len(words) - 1 else "")

        if current == "" or font.size(current + piece)[0] <= max_width:
            current += piece
        else:
            lines.append(current)
            current = piece

    if current:
        lines.append(current)

    return lines


def build_layout(text, font):
    """محاسبه مختصات نمایش تک‌تک حروف."""

    lines = wrap_text(
        text,
        font,
        TEXT_RECT.width - 40
    )

    line_height = font.get_linesize() + 14
    positions = []
    y = TEXT_RECT.y + 25

    for line in lines:
        x = TEXT_RECT.x + 20

        for ch in line:
            positions.append((x, y))
            x += font.size(ch)[0]

        y += line_height

    return positions