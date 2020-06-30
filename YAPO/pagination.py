from rest_framework import pagination
from rest_framework.response import Response


class HeaderLimitOffsetPagination(pagination.LimitOffsetPagination):
    def get_paginated_response(self, data):
        next_url = self.get_next_link()
        previous_url = self.get_previous_link()
        count = self.count
        page_size = self.limit

        if next_url is not None and previous_url is not None:
            link = '<{next_url}>; rel="next", <{previous_url}>; rel="prev" ,<{count}>; rel="count", <{page_size}>; rel="page_size"'
        elif next_url is not None:
            link = '<{next_url}>; rel="next", <{count}>; rel="count", <{page_size}>; rel="page_size"'
        elif previous_url is not None:
            link = '<{previous_url}>; rel="prev", <{count}>; rel="count", <{page_size}>; rel="page_size"'
        else:
            link = ''

        link = link.format(next_url=next_url, previous_url=previous_url, count=count, page_size=page_size)
        headers = {'Link': link} if link else {}

        return Response(data, headers=headers)
