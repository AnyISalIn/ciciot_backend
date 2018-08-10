from user import views
from django.urls import path

app_name = 'user'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('pc-gt/', views.GtValidateView.as_view(), name='gt-validate'),
    path(r'active/<uidb64>/<token>/', views.ActiveView.as_view(), name='active'),
]
