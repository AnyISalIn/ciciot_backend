from django import template
from article.models import Like, Article

register = template.Library()


@register.simple_tag
def is_like(user, article):
    return True if article.like_set.filter(user__id=user.id).first() else False


@register.filter
def highlighted(content, keyword):
    highlighted_text = Article.highlighted(content, keyword)
    if highlighted_text:
        return highlighted_text
    return content[:36]
