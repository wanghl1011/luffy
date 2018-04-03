from rest_framework.pagination import PageNumberPagination
class MyPageNumberPagination(PageNumberPagination):
    # 默认每页显示几条数据
    page_size = 5
    # 在URL中GET数据中的key，用来修改每页显示数据数
    page_size_query_param = 'size'
    # 定义每页显示数据的最大数
    max_page_size = 5
    # 在URL中GET数据的key，用来指定查看第几页的数据
    page_query_param = 'page'