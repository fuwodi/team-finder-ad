import io
import random

from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

AVATAR_COLORS = [
    (91, 141, 184),
    (120, 154, 130),
    (176, 137, 104),
    (158, 123, 168),
    (107, 153, 178),
    (186, 120, 120),
    (130, 150, 120),
    (150, 130, 160),
]


def generate_avatar_image(letter: str) -> ContentFile:
    size = (128, 128)
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
