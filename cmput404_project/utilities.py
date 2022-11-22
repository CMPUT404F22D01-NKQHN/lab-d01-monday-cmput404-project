import uuid
from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = "size"

def gen_id():
    return uuid.uuid4().hex