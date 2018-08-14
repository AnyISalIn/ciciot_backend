from article.models import Article
from rest_framework.serializers import ModelSerializer, CharField


class ArticleSerializer(ModelSerializer):
    url = CharField(source='get_absolute_url')

    class Meta:
        model = Article
        fields = ('id', 'title', 'url', 'pub_date')
