from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ForceReply,
)
from pyrogram import enums


INLINE_BUTTON_TYPES = {
    "callback_data",
    "url",
    "switch_inline_query",
    "switch_inline_query_current_chat",
    "callback_game",
    "web_app",
    "login_url",
    "user_id",
    "copy_text",
}


def ikb(rows=None):
    """
    Create an InlineKeyboardMarkup from a list of lists of buttons.

    Supports:
        "text"
        InlineKeyboardButton(...)
        {"text": "...", "value": "...", "style": enums.ButtonStyle.SUCCESS}
        ("text", "callback")
        ("text", "callback", enums.ButtonStyle.SUCCESS)
        ("text", "callback", enums.ButtonStyle.SUCCESS, "custom_emoji_id")
        ("text", "https://example.com", "url")
        ("text", "https://example.com", "url", enums.ButtonStyle.PRIMARY)
        ("text", "callback", "callback_data", enums.ButtonStyle.SUCCESS, "custom_emoji_id")
    """
    if rows is None:
        rows = []

    lines = []

    for row in rows:
        line = []

        for button in row:
            if isinstance(button, InlineKeyboardButton):
                line.append(button)
                continue

            if isinstance(button, str):
                button = btn(button, button)

            elif isinstance(button, dict):
                button = btn(**button)

            elif isinstance(button, (list, tuple)):
                button = _btn_from_tuple(button)

            else:
                raise TypeError(f"Unsupported inline button type: {type(button).__name__}")

            line.append(button)

        lines.append(line)

    return InlineKeyboardMarkup(inline_keyboard=lines)


def _btn_from_tuple(data):
    if len(data) < 2:
        raise ValueError("Inline button tuple/list must contain at least text and value")

    text = data[0]
    value = data[1]

    button_type = "callback_data"
    style = enums.ButtonStyle.DEFAULT
    icon_custom_emoji_id = None

    for item in data[2:]:
        if isinstance(item, enums.ButtonStyle):
            style = item
        elif isinstance(item, str):
            if item in INLINE_BUTTON_TYPES:
                button_type = item
            else:
                icon_custom_emoji_id = item
        elif item is None:
            continue
        else:
            icon_custom_emoji_id = str(item)

    return btn(
        text=text,
        value=value,
        type=button_type,
        style=style,
        icon_custom_emoji_id=icon_custom_emoji_id
    )


def btn(
    text,
    value,
    type="callback_data",
    style=enums.ButtonStyle.DEFAULT,
    icon_custom_emoji_id=None
):
    """
    Create an InlineKeyboardButton.
    """
    kwargs = {
        type: value,
        "style": style,
    }

    if icon_custom_emoji_id is not None:
        kwargs["icon_custom_emoji_id"] = icon_custom_emoji_id

    return InlineKeyboardButton(text, **kwargs)


def bki(keyboard):
    lines = []

    for row in keyboard.inline_keyboard:
        line = []

        for button in row:
            button = ntb(button)
            line.append(button)

        lines.append(line)

    return lines


def ntb(button):
    value = None
    btn_type = "callback_data"

    for candidate in [
        "callback_data",
        "url",
        "switch_inline_query",
        "switch_inline_query_current_chat",
        "callback_game",
        "web_app",
        "login_url",
        "user_id",
        "copy_text",
    ]:
        value = getattr(button, candidate, None)

        if value:
            btn_type = candidate
            break

    result = [button.text, value]

    if btn_type != "callback_data":
        result.append(btn_type)

    if getattr(button, "style", enums.ButtonStyle.DEFAULT) != enums.ButtonStyle.DEFAULT:
        result.append(button.style)

    if getattr(button, "icon_custom_emoji_id", None):
        result.append(button.icon_custom_emoji_id)

    return result


def kb(rows=None, **kwargs):
    if rows is None:
        rows = []

    lines = []

    for row in rows:
        line = []

        for button in row:
            if isinstance(button, KeyboardButton):
                pass
            elif isinstance(button, str):
                button = KeyboardButton(button)
            elif isinstance(button, dict):
                button = KeyboardButton(**button)
            else:
                raise TypeError(f"Unsupported keyboard button type: {type(button).__name__}")

            line.append(button)

        lines.append(line)

    return ReplyKeyboardMarkup(keyboard=lines, **kwargs)


kbtn = KeyboardButton


def force_reply(selective=True):
    return ForceReply(selective=selective)


def array_chunk(input_array, size):
    return [input_array[i: i + size] for i in range(0, len(input_array), size)]
