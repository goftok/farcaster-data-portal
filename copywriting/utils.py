import re


def clean_cast_text(cast_text):
    # Remove emojis
    cast_text = re.sub(r"[^\w\s,]", "", cast_text)  # Remove anything except word characters and spaces
    return cast_text.lower().strip()
