from article.models import Article
from article.serializers import ArticleSerializer

from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from django.views.decorators.csrf import csrf_exempt


class APIArticleList(mixins.ListModelMixin,
                     generics.GenericAPIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    pagination_class = LimitOffsetPagination

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
