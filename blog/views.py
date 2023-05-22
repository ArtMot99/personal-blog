from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Post


def index(request) -> HttpResponse:
    """Index view for the blog project home page"""
    posts = (
        Post.objects.select_related("author")
        .prefetch_related("categories")
        .annotate(num_comments=Count("comments"))
    )
    context = {"posts": posts}

    return render(request, "blog/index.html", context=context)
