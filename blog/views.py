from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render
from blog.forms import PostFilterForm, PostSearchForm
from blog.models import Post


def index(request) -> HttpResponse:
    """Index view for the blog project home page"""
    post_list = (
        Post.objects.select_related("author")
        .prefetch_related("categories")
        .annotate(num_comments=Count("comments"))
    )
    filter_form = PostFilterForm()
    search_form = PostSearchForm()

    if request.method == "GET":
        filter_form = PostFilterForm(request.GET)
        search_form = PostSearchForm(request.GET)

        if filter_form.is_valid():
            category = filter_form.cleaned_data["category"]
            if category:
                post_list = post_list.filter(categories=category)

        if search_form.is_valid():
            search_term = search_form.cleaned_data["search_term"]
            if search_term:
                post_list = post_list.filter(
                    Q(title__icontains=search_term) | Q(content__icontains=search_term)
                )

    paginator = Paginator(post_list, 4)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
        "filter_form": filter_form,
        "search_form": search_form,
    }

    return render(request, "blog/index.html", context=context)
