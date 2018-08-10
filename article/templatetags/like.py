from django import template
from article.models import Like

register = template.Library()


@register.simple_tag
def is_like(user, article):
    return True if article.like_set.filter(user__id=user.id).first() else False
