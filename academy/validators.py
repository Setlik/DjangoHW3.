import re

from django.core.exceptions import ValidationError


def validate_youtube_url(value):
    """Валидатор для проверки URL на соответствие youtube.com."""

    youtube_url = r"^(https?://)?(www\.)?(youtube\.com)/.+$"
    if not re.match(youtube_url, value):
        raise ValidationError(
            ("Ссылка должна быть на видео youtube.com"),
            params={"value": value},
        )
