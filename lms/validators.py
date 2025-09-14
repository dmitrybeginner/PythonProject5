from rest_framework.serializers import ValidationError


def youtube_link_validator(value):
    """
    Валидатор, который проверяет, что ссылка ведет на youtube.com.
    """
    if value and 'youtube.com' not in value:
        raise ValidationError('Ссылка должна вести на youtube.com')
