# Compatibility readers for legacy keyboard button constructors.
# Telegram can still send these old constructors in incoming updates.
#
# Do not map old constructor IDs directly to the new generated classes in all.py
# when their binary layout is different. Use small readers instead.

try:
    from io import BytesIO
    from .core.primitives import String
    from .types import KeyboardButton

    class _LegacyKeyboardButton:
        @staticmethod
        def read(b: BytesIO, *args):
            return KeyboardButton(text=String.read(b))

    # keyboardButton#a2fa4880 text:string = KeyboardButton;
    objects.setdefault(0xa2fa4880, _LegacyKeyboardButton)

except Exception:
    pass


try:
    from io import BytesIO
    from .core.primitives import String
    from .types import KeyboardButtonUrl

    class _LegacyKeyboardButtonUrl:
        @staticmethod
        def read(b: BytesIO, *args):
            text = String.read(b)
            url = String.read(b)
            return KeyboardButtonUrl(text=text, url=url)

    # keyboardButtonUrl#258aff05 text:string url:string = KeyboardButton;
    objects.setdefault(0x258aff05, _LegacyKeyboardButtonUrl)

except Exception:
    pass


try:
    from io import BytesIO
    from .core.primitives import String
    from .types import KeyboardButtonRequestPhone

    class _LegacyKeyboardButtonRequestPhone:
        @staticmethod
        def read(b: BytesIO, *args):
            return KeyboardButtonRequestPhone(text=String.read(b))

    # keyboardButtonRequestPhone#b16a6c29 text:string = KeyboardButton;
    objects.setdefault(0xb16a6c29, _LegacyKeyboardButtonRequestPhone)

except Exception:
    pass


try:
    from io import BytesIO
    from .core.primitives import String
    from .types import KeyboardButtonRequestGeoLocation

    class _LegacyKeyboardButtonRequestGeoLocation:
        @staticmethod
        def read(b: BytesIO, *args):
            return KeyboardButtonRequestGeoLocation(text=String.read(b))

    # keyboardButtonRequestGeoLocation#fc796b3f text:string = KeyboardButton;
    objects.setdefault(0xfc796b3f, _LegacyKeyboardButtonRequestGeoLocation)

except Exception:
    pass


try:
    from .types import KeyboardButtonCallback

    # keyboardButtonCallback#35bbdb6b flags:# requires_password:flags.0?true text:string data:bytes = KeyboardButton;
    objects.setdefault(0x35bbdb6b, KeyboardButtonCallback)

except Exception:
    pass


try:
    from .types import KeyboardButtonStyle

    # keyboardButtonStyle#4fdd3430 ...
    objects.setdefault(0x4fdd3430, KeyboardButtonStyle)

except Exception:
    pass
