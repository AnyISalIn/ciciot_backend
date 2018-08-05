from article.views import ListView, DetailView, SearchView
from django.conf.urls import url, include

app_name = 'article'

urlpatterns = [
    url(r'^$', ListView.as_view(), name='list'),
    url(r'^search/$', SearchView.as_view(), name='search'),
    url(r'(?P<pk>[0-9]+)/$', DetailView.as_view(), name='detail')
]
