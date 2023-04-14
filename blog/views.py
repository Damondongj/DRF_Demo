from rest_framework import viewsets
from rest_framework import permissions
from django_filters.rest_framework import DjangoFilterBackend

from .models import Article
from .filters import ArticleFilter
from .serializers import ArticleSerializer
from .pagination import MyPageNumberPagination


class ArticleViewSet(viewsets.ModelViewSet):
    # 用一个视图集替代ArticleList和ArticleDetail两个视图
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = MyPageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = ArticleFilter
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    THROTTLE_RATES = {
        "anon": "5/min",
        "user": "30/min"
    }

    # 自行添加，将request.user与author绑定
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        print(res)
        return res
