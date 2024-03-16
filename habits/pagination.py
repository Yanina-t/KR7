# habits/pagination.py

from rest_framework.pagination import PageNumberPagination


class HabitListPagination(PageNumberPagination):
    """
    Пагинация списка привычек.
    """
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 10
