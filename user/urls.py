import user.views as view
from django.conf.urls import url, include
from django.urls import path

app_name = 'user'

urlpatterns = [
    path('register/', view.RegisterView.as_view(), name='register'),
    path('login/', view.LoginView.as_view(), name='login'),
    path('logout/', view.LogoutView.as_view(), name='logout'),
    path('pc-gt/', view.GtValidateView.as_view(), name='gt-validate'),
    path(r'active/<uidb64>/<token>/', view.ActiveView.as_view(), name='active'),
]
