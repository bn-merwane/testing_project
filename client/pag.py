from rest_framework.pagination import CursorPagination


class PostCursorPaginationNormal(CursorPagination):
    page_size = 1  # Number of posts per page
    cursor_query_param = 'cursor'  # Query parameter for the cursor
    ordering = 'start_at'  # Order posts by creation date, newest first

