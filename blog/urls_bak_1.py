from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

article_list = views.ArticleViewSet.as_view(
    {
        "get": "list",
        "post": "create"
    }
)

article_detail = views.ArticleViewSet.as_view(
    {
        "get": "retrieve",  # 只处理get请求，获取单个记录
    }
)

urlpatterns = [
    re_path("^articles/$", article_list),
    re_path("^articles/(?P<pk>[0-9]+)$", article_detail)
]

# format_suffix_patterns 是一个辅助函数，用于将API视图的url模式与可选的格式后缀匹配，以便在API请求中指定响应的内容类型
urlpatterns = format_suffix_patterns(urlpatterns)
