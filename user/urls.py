from user.views import RegisterView, LoginView, LogoutView, ActiveView
from django.conf.urls import url, include
from django.urls import path

app_name = 'user'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path(r'active/<uidb64>/<token>/', ActiveView.as_view(), name='active'),
]
