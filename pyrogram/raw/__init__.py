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


# Compatibility reader for legacy keyboardButton#a2fa4880.
# Telegram can still send this old constructor in incoming updates.
#
# Old constructor:
#   keyboardButton#a2fa4880 text:string = KeyboardButton;
#
# New constructor:
#   keyboardButton#7d170cff flags:# style:flags.10?KeyboardButtonStyle text:string = KeyboardButton;
#
# Do not map 0xa2fa4880 directly to raw.types.KeyboardButton in all.py,
# because the new KeyboardButton reader expects flags first.
try:
    from io import BytesIO

    from .core.primitives import String
    from .types import KeyboardButton

    class _LegacyKeyboardButton:
        @staticmethod
        def read(b: BytesIO, *args):
            return KeyboardButton(text=String.read(b))

    objects[0xa2fa4880] = _LegacyKeyboardButton

except Exception:
    pass