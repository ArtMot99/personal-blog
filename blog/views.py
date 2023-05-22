from django.core.paginator import Paginator
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Post


def index(request) -> HttpResponse:
    """Index view for the blog project home page"""
    post_list = (
        Post.objects.select_related("author")
        .prefetch_related("categories")
        .annotate(num_comments=Count("comments"))
    )
    paginator = Paginator(post_list, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}

    return render(request, "blog/index.html", context=context)
