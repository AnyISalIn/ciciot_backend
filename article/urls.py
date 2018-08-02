from article.views import ListView, DetailView
from django.conf.urls import url, include

app_name = 'article'

urlpatterns = [
    url(r'^$', ListView.as_view(), name='list'),
    url(r'(?P<pk>[0-9]+)/$', DetailView.as_view(), name='detail')
]
