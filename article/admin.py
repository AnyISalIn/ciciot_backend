from django.contrib import admin
from django.conf import settings
from article.models import Article, Category, Author


class ArticleAdmin(admin.ModelAdmin):
    readonly_fields = ['content_preview']
    list_display = ['title', 'author', 'pub_date', 'is_public']
    list_filter = ['pub_date', 'author', 'categorise']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category)
admin.site.register(Author)
admin.site.site_header = settings.ADMIN_SITE_HEADER
