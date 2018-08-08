from django.urls import path
from article.views import ListView, DetailView, SearchView

app_name = 'article'

urlpatterns = [
    path('', ListView.as_view(), name='list'),
    path(r'search/', SearchView.as_view(), name='search'),
    path(r'<int:pk>', DetailView.as_view(), name='detail')
]
