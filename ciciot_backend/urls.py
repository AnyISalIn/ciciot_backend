"""ciciot_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.urls import path
from django.contrib import admin
from article.views import SiteIndexView
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from article.models import Article

urlpatterns = [
                  path('', SiteIndexView.as_view(), name='home'),
                  path('admin/', admin.site.urls),
                  path('ckeditor/', include('ckeditor_uploader.urls')),
                  path('articles/', include('article.urls.view_urls', 'article')),
                  path('api/', include('article.urls.api_urls')),
                  path('user/', include('user.urls', 'user')),
                  path('sitemap.xml', sitemap, {'sitemaps': {'article': GenericSitemap(dict(
                      queryset=Article.objects.all(), date_field='pub_date'), priority=0.6)}},
                       name='django.contrib.sitemaps.views.sitemap'),
              ] + static('/uploads', document_root=settings.CKEDITOR_UPLOAD_PATH)
urlpatterns += staticfiles_urlpatterns()
