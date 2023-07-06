class RecordNotExistDb(Exception):
    """Запрошенная запись в БД не найдена."""

    pass


class CreateRecordExistDb(Exception):
    """Создаваемая запись уже существует в БД."""
    pass


class AccessDenied(Exception):
    """Доступ запрещен."""
    pass


class LikeDenied(Exception):
    """Голосовать запрещено."""
    pass
