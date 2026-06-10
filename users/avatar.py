import io
import random

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

AVATAR_SIZE = 128

AVATAR_COLOR_STEEL_BLUE = (91, 141, 184)
AVATAR_COLOR_SAGE_GREEN = (120, 154, 130)
AVATAR_COLOR_TAN = (176, 137, 104)
AVATAR_COLOR_LAVENDER = (158, 123, 168)
AVATAR_COLOR_BLUE_GRAY = (107, 153, 178)
AVATAR_COLOR_DUSTY_ROSE = (186, 120, 120)
AVATAR_COLOR_OLIVE_GREEN = (130, 150, 120)
AVATAR_COLOR_MAUVE = (150, 130, 160)

AVATAR_COLORS = [
    AVATAR_COLOR_STEEL_BLUE,
    AVATAR_COLOR_SAGE_GREEN,
    AVATAR_COLOR_TAN,
    AVATAR_COLOR_LAVENDER,
    AVATAR_COLOR_BLUE_GRAY,
    AVATAR_COLOR_DUSTY_ROSE,
    AVATAR_COLOR_OLIVE_GREEN,
    AVATAR_COLOR_MAUVE,
]


def generate_avatar_image(letter: str) -> ContentFile:
    size = (AVATAR_SIZE, AVATAR_SIZE)
    color = random.choice(AVATAR_COLORS)
    image = Image.new("RGB", size, color)
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype("arial.ttf", 64)
    except OSError:
        font = ImageFont.load_default()

    text = (letter or "?")[0].upper()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    position = ((size[0] - text_width) / 2, (size[1] - text_height) / 2 - 8)
    draw.text(position, text, fill=(255, 255, 255), font=font)

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)
    return ContentFile(buffer.read(), name="avatar.png")
