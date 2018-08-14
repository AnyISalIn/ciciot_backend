from django.urls import path
from article import views

app_name = 'article'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='list'),
    path(r'search/', views.ArticleSearchView.as_view(), name='search'),
    path(r'like/<int:pk>', views.ArticleLikeView.as_view(), name='like'),
    path(r'<int:pk>', views.ArticleDetailView.as_view(), name='detail')
]
