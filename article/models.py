from bs4 import BeautifulSoup

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return '<{}>'.format(self.name)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '<{} Like {}>'.format(self.user.username, self.article.title)


class Article(models.Model):
    title = models.CharField(max_length=50)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    content = RichTextUploadingField()
    categorise = models.ManyToManyField('Category')
    view = models.IntegerField(default=0)
    is_public = models.BooleanField(default=False)
    pub_date = models.DateTimeField()

    def content_preview(self):
        return mark_safe(self.content)

    @property
    def preview_picture(self):
        bs_obj = BeautifulSoup(self.content, 'lxml')
        img_tag = bs_obj.img
        if not img_tag:
            return settings.DEFAULT_PREVIEW_PICTURE
        return img_tag.attrs['src']

    @property
    def headline(self):
        return BeautifulSoup(self.content, 'lxml').p.text[:36]

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return '<Article {}>'.format(self.title)


class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return '<{}>'.format(self.name)
