from rest_framework import pagination
from rest_framework.response import Response


class TweetsPagination(pagination.PageNumberPagination):
    page_size = 2
    max_page_size = 10
    page_query_param = 'page'
    page_size_query_param = 'page_size'

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })

