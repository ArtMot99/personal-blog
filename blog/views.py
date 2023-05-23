from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import DetailView

from blog.forms import PostFilterForm, PostSearchForm, CommentForm
from blog.models import Post, Comment


def index(request) -> HttpResponse:
    """Index view for the blog project home page"""
    post_list = (
        Post.objects.select_related("author")
        .prefetch_related("categories")
        .annotate(num_comments=Count("comments"))
        .order_by("-created_at")
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


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = CommentForm()
        context["comments"] = Comment.objects.filter(post=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                text=form.cleaned_data["text"], post=self.object, author=request.user
            )
            comment.save()
            return self.get(request, *args, **kwargs)
        else:
            return self.render_to_response(self.get_context_data(form=form))
