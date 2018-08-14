from article.api import APIArticleList

from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'api_article'

urlpatterns = [
    path('articles/', APIArticleList.as_view(), name='list')
]

urlpatterns = format_suffix_patterns(urlpatterns)
