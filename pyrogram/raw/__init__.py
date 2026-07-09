#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from importlib import import_module

from . import types, functions, base, core
from .all import objects


for k, v in objects.items():
    path, name = v.rsplit(".", 1)
    objects[k] = getattr(import_module(path), name)


# Compatibility readers for legacy keyboard button constructors.
# Some old constructors do not have flags/style, so they must not be parsed
# directly by the new generated classes.

try:
    from io import BytesIO

    from .core.primitives import Int, String, Bytes
    from .types import (
        KeyboardButton,
        KeyboardButtonUrl,
        KeyboardButtonCallback,
        KeyboardButtonRequestPhone,
        KeyboardButtonRequestGeoLocation,
    )

    class _LegacyKeyboardButton:
        @staticmethod
        def read(b: BytesIO, *args):
            return KeyboardButton(text=String.read(b))

    class _LegacyKeyboardButtonUrl:
        @staticmethod
        def read(b: BytesIO, *args):
            text = String.read(b)
            url = String.read(b)
            return KeyboardButtonUrl(text=text, url=url)

    class _LegacyKeyboardButtonRequestPhone:
        @staticmethod
        def read(b: BytesIO, *args):
            return KeyboardButtonRequestPhone(text=String.read(b))

    class _LegacyKeyboardButtonRequestGeoLocation:
        @staticmethod
        def read(b: BytesIO, *args):
            return KeyboardButtonRequestGeoLocation(text=String.read(b))

    # Old callback constructor already has flags, so the new class can read it.
    # But keep this explicit for compatibility.
    objects[0x35bbdb6b] = KeyboardButtonCallback

    # These old constructors do not have style flags.
    # Override direct all.py mapping with safe legacy readers.
    objects[0xa2fa4880] = _LegacyKeyboardButton
    objects[0x258aff05] = _LegacyKeyboardButtonUrl
    objects[0xb16a6c29] = _LegacyKeyboardButtonRequestPhone
    objects[0xfc796b3f] = _LegacyKeyboardButtonRequestGeoLocation

except Exception:
    pass
