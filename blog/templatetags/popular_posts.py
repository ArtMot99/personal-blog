from django import template
from django.db.models import Count

from blog.models import Post

register = template.Library()


@register.simple_tag
def get_popular_posts(count=5):
    popular_posts = Post.objects.annotate(
        num_comments=Count("comments")
    ).order_by("-num_comments")[:count]

    return popular_posts
