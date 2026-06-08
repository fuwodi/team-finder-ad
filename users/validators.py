import re

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def normalize_phone(phone: str) -> str:
    digits = re.sub(r"\D", "", phone)
    if len(digits) == 11 and digits.startswith("8"):
        return f"+7{digits[1:]}"
    if len(digits) == 11 and digits.startswith("7"):
        return f"+7{digits[1:]}"
    return phone


def validate_phone_format(phone: str) -> str:
    normalized = normalize_phone(phone)
    if re.fullmatch(r"\+7\d{10}", normalized):
        return normalized
    if re.fullmatch(r"8\d{10}", phone.strip()):
        return normalize_phone(phone)
    raise ValidationError(
        "Номер телефона должен быть в формате 8XXXXXXXXXX или +7XXXXXXXXXX."
    )


def validate_github_url(url: str) -> str:
    if not url:
        return url
    validator = URLValidator()
    validator(url)
    if "github.com" not in url.lower():
        raise ValidationError("Ссылка должна вести на GitHub.")
    return url
