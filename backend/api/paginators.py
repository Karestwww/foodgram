from rest_framework.pagination import LimitOffsetPagination


class StandardResultsSetPagination(LimitOffsetPagination):
    """Пагинатор для моделей модуля."""

    page_size = 6
    default_limit = page_size
    max_limit = page_size
#    max_page_size = 1000
