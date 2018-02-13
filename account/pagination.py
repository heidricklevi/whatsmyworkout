from rest_framework.pagination import PageNumberPagination


class CustomExercisesPagination(PageNumberPagination):
    page_size = 250