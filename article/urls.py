from django.urls import path
from article import views

app_name = 'article'

urlpatterns = [
    path('', views.ListView.as_view(), name='list'),
    path(r'search/', views.SearchView.as_view(), name='search'),
    path(r'like/<int:pk>', views.LikeView.as_view(), name='like'),
    path(r'<int:pk>', views.DetailView.as_view(), name='detail')
]
